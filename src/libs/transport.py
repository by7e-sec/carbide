import os

from colorama import Fore, Style
from loguru import logger

from . import agents_registry
from .agent import Agent
from .blueprint.blueprint import Blueprint


class Transport:
    bp: Blueprint
    source_files: list[tuple[str, str]] = []
    agent: Agent | None
    auth = []

    def __init__(self, bp: Blueprint) -> None:
        self.bp = bp
        self.source_files = []

    def __filter_items(self, filters: list[str], item: str) -> bool:
        """
        Check if an item should be filtered out.

        Returns
            bool
        """
        for flt in filters:
            if flt in item:
                return True
        return False

    def index_source_folder(self) -> None:
        """
        Readies files to be transferred by indexing folder structure,
        and stripping the source folder from the destination
        """
        src: dict[str, str] = self.bp.get_source()
        source_files: list[tuple[str, str]] = []

        if src["type"] == "folder":
            filters: list[str] = []
            if "filter" in src:
                filters = src["filter"]

            for root, dirs, files in os.walk(src["folder"], topdown=True):
                pth = root.replace(src["folder"], "")
                filtered = self.__filter_items(filters, pth)

                if not filtered:
                    for d in dirs:
                        if not self.__filter_items(filters, d):
                            path: str = os.path.join(root, d)
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
        else:
            source_files = []
            logger.warning("Invalid option. Skipping.")

        self.source_files = source_files

    def init_agent(self, auth_name: str, machine: str) -> Agent | None:
        """
        Instantiate protocol and authenticate remote machine
        """
        agent: Agent | None = None
        conn_type: str = self.bp.get_connection_type(machine)
        if conn_type in agents_registry.get_agents():
            agent = agents_registry.instance_agent(conn_type)
        else:
            raise Exception(f"oops! {machine} returned connecton type {conn_type}")

        # Authenticate agent if possible
        auth = self.bp.get_auth(auth_name, machine)
        if agent and self.bp.is_valid():
            agent.authenticate(auth)

        return agent

    def is_client_active(self, agent: Agent | None) -> bool:
        """
        Check if client has been initialized / authenticated
        """

        if not agent:
            return False

        return bool(agent.client)

    def copy_files(self, agent: Agent | None, dest_folder: str, machine_name: str) -> bool:
        """
        Copy files
        """
        if agent:
            if self.source_files == []:
                logger.warning("Nothing to do.")
            else:
                return agent.copy_files(self.source_files, dest_folder, machine_name)
        else:
            logger.critical("Agent hasn't been initiated properly!")

        return False

    def run(self):
        try:
            if self.bp.is_source_local():
                self.index_source_folder()
            for dest in self.bp.get_destinatons():
                if dest.is_valid():
                    if not dest.is_local():
                        agent = self.init_agent(dest.auth(), dest.get_machine())
                        if self.is_client_active(agent):
                            self.run_commands(agent, dest.get_remote_commands("before"))
                            files_cp: bool = self.copy_files(agent, dest.get_folder(), dest.get_machine())
                            if not files_cp:
                                logger.warning("Error in copying files! Skipping further processing!")
                                continue
                            self.run_commands(agent, dest.get_remote_commands("after"))
                        else:
                            logger.warning("Client has not been initiated! Skipping further processing!")
                    else:
                        print(f"{dest.get_machine()}: local handling isn't implemented yet")
                else:
                    print(
                        f"{dest.get_machine()}: {Fore.RED}Destination isn't valid! "
                        + f"({dest.show_destination_error()}){Style.RESET_ALL}"
                    )
        except PermissionError as pe:
            logger.error(f"There was a permission error while running the blueprint: {pe}. Do you need to be root?")
        except Exception as e:
            logger.error(f"There was an error executing the blueprint: {e}")

    def run_commands(self, agent: Agent | None, commands: dict[str, list[str]]) -> None:
        """
        Execute remote or local commands / scripts
        """
        if agent:
            for cmd in ["commands", "scripts"]:
                if commands[cmd] != []:
                    logger.debug(f"Executing remote {cmd}:")
                    agent.run_commands(commands[cmd])

        else:
            logger.critical("Agent hasn't been initiated properly!")
