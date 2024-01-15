import os

from loguru import logger

from .agents import sftp_agent
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
        self.auth = {}

        self.__init_agent()
        self.__index_source_files()

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
            try:
                source_files = []
                filters = []
                if "filter" in src:
                    filters = src["filter"]

                for root, dirs, files in os.walk(src["folder"], topdown=True):
                    pth = root.replace(src["folder"], "")
                    filtered = False
                    for flt in filters:
                        if flt in pth:
                            filtered = True

                    if not filtered:
                        for d in dirs:
                            if not self.__filter_items(filters, d):
                                path = os.path.join(root, d)
                                source_files.append(
                                    (
                                        path,
                                        path[len(src["folder"]) :],
                                    )
                                )

                        for file in files:
                            path = os.path.join(root, file)
                            source_files.append(
                                (
                                    path,
                                    path[len(src["folder"]) :],
                                )
                            )
            except Exception as e:
                logger.critical(f"Unable to copy data to destination!\n{e}")

        self.source_files = source_files

    def authenticate(self, machine: str) -> None:
        """
        Authenticate remote machine
        """
        self.auth = self.bp.get_auth_dict(machine)
        if self.agent:
            self.agent.authenticate(self.auth)

    def copy_files(self, dest_folder: str) -> None:
        """
        Copy files
        """
        if self.agent:
            self.agent.copy_files(self.source_files, dest_folder)
        else:
            logger.critical(f"Agent hasn't been initiated properly!")
