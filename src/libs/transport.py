import os

from loguru import logger

from agents import sftp_agent

from .blueprint import Blueprint


class Transport:
    bp: Blueprint = None
    source_files: list = []
    agent = None
    auth = []

    def __init__(self, bp: Blueprint) -> None:
        self.bp = bp
        self.source_files = []
        self.agent = None

        self.__init_agent()
        try:
            self.__index_source_files()
        except PermissionError as pe:
            raise PermissionError(pe)
        except Exception as e:
            raise Exception(e)

    def __init_agent(self) -> None:
        """
        Init transport agent (SFTP, rsync, local,...)
        """
        kind = self.bp.get_kind()
        if kind == "sftp":
            self.agent = sftp_agent.SftpAgent()

    def __filter_items(self, filters: list, item: str) -> bool:
        """
        Check if an item should be filtered out.

        Returns
            bool
        """
        for flt in filters:
            if flt in item:
                return True
        return False

    def __index_source_files(self):
        """
        Readies files to be transferred by indexing folder structure,
        and stripping the source folder from the destination
        """
        src = self.bp.get_source()
        if src["type"] == "folder":
            source_files = []
            filters = []
            if "filter" in src:
                filters = src["filter"]

            for root, dirs, files in os.walk(src["folder"], topdown=True):
                pth = root.replace(src["folder"], "")
                filtered = self.__filter_items(filters, pth)

                if not filtered:
                    for d in dirs:
                        if not self.__filter_items(filters, d):
                            path = os.path.join(root, d)
                            if not os.access(path, os.R_OK):
                                raise PermissionError(f"Unable to access: {path}")

                            source_files.append(
                                (
                                    path,
                                    path[len(src["folder"]) :],
                                )
                            )

                    for file in files:
                        path = os.path.join(root, file)
                        if not os.access(path, os.R_OK):
                            raise PermissionError(f"Unable to access: {path}")

                        source_files.append(
                            (
                                path,
                                path[len(src["folder"]) :],
                            )
                        )

        self.source_files = source_files

    def authenticate(self, auth_name: str, machine: str) -> None:
        """
        Authenticate remote machine
        """
        auth = self.bp.get_auth_dict(auth_name, machine)
        if self.agent and self.bp.is_valid():
            self.agent.authenticate(auth)

    def is_client_active(self):
        """
        Check if client has been initialized / authenticated
        """
        return bool(self.agent.client)

    def copy_files(self, dest_folder: str) -> None:
        """
        Copy files
        """
        if self.agent:
            if self.source_files == []:
                logger.warning("Nothing to do.")
            else:
                self.agent.copy_files(self.source_files, dest_folder)
        else:
            logger.critical(f"Agent hasn't been initiated properly!")
