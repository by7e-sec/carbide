import sys
import threading
from optparse import Values
from threading import Thread

from colorama import Fore, Style
from loguru import logger

from libs.blueprint.destinations import Destinations

from .blueprint.blueprint import Blueprint
from .blueprints import Blueprints
from .config import Config
from .transport import Transport


class Processor:
    blueprints: Blueprints
    opts: Values
    conf: Config

    def __init__(self, conf: Config, opts: Values) -> None:
        self.blueprints = Blueprints(conf, [] if opts.listblueprints else opts.blueprint)
        self.opts = opts
        self.conf = conf

        if opts.listblueprints:
            self.list_blueprints()

    def list_blueprints(self) -> None:
        """
        Pretty display the list of blueprints by name, validity, activity, type,
        and description, and exit.
        """
        # Colors
        bright_green = Style.BRIGHT + Fore.GREEN
        dim_red = Style.DIM + Fore.RED

        bps: dict[str, dict[str, str | list[Destinations]]] = self.blueprints.list_all()
        print(f"{Style.BRIGHT}{Fore.MAGENTA}Available blueprints:")
        for bp in bps:
            is_valid = bright_green + "Valid" if bps[bp]["valid"] else dim_red + "Not valid"
            is_active = bright_green + "Active" if bps[bp]["active"] else dim_red + "Inactive"
            is_valid = is_valid + Style.RESET_ALL
            is_active = is_active + Style.RESET_ALL

            print(f"{Style.BRIGHT}{Fore.YELLOW}{bp}: {is_valid} {Fore.WHITE} || {is_active}")
            print(f"{Style.BRIGHT}{Fore.BLUE} Kind: " + str(bps[bp]["kind"]) if bps[bp]["kind"] != "" else "fallback")
            if bps[bp]["description"] != "":
                description: str = str(bps[bp]["description"])
                print(f"{Style.DIM}{Fore.WHITE} # {Fore.MAGENTA}{description}")

            print(Style.BRIGHT + Fore.LIGHTBLUE_EX + " Destinations: " + Style.RESET_ALL)
            dests: list[Destinations] = bps[bp]["destinations"]
            for dest in dests:
                is_destination_valid: str = bright_green + "Valid" if dest.is_valid() else dim_red + "Not valid"
                is_destination_valid = is_destination_valid + Style.RESET_ALL
                machine_name: str = str(dest.get_machine())
                print(f"{Style.BRIGHT}{Fore.WHITE}  > {machine_name} | " + is_destination_valid)

            print(Style.RESET_ALL)

        sys.exit(0)

    def run_blueprint(self, bp: Blueprint) -> None:
        """
        Execute seperate blueprint
        """
        if bp.is_active():
            if bp.is_source_local():
                try:
                    tx = Transport(bp)
                    for dest in bp.get_destinatons():
                        if dest.is_valid():
                            if not dest.is_local():
                                tx.authenticate(dest.auth(), dest.get_machine())
                                if tx.is_client_active():
                                    tx.run_commands(dest.get_remote_commands("before"))
                                    files_cp = tx.copy_files(dest.get_folder(), dest.get_machine())
                                    if not files_cp:
                                        logger.warning("Error in copying files! Skipping further processing!")
                                        continue
                                    tx.run_commands(dest.get_remote_commands("after"))
                                else:
                                    logger.warning("Client has not been initiated! Skipping further processing!")
                            else:
                                print(f"{dest.get_machine()}: local handling isn't implemented yet")
                        else:
                            print(
                                f"{dest.get_machine()}: {Fore.RED}Destination isn't valid! ({dest.show_destination_error()}){Style.RESET_ALL}"
                            )
                except PermissionError as pe:
                    logger.error(f"There was a permission error while running the blueprint: {pe}. Do you need to be root?")
                except Exception as e:
                    logger.error(f"There was an error executing the blueprint: {e}")

    def run(self) -> None:
        """
        Run blueprints in threaded environment if executed via CLI
        """
        threads: list[threading.Thread] = []
        # execute threads
        for bp in self.blueprints.get_blueprints():
            t: Thread = threading.Thread(target=self.run_blueprint, args=(bp,))
            threads.append(t)

        # Run threads
        for t in threads:
            t.start()

        # Wait until threads are done
        for t in threads:
            t.join()
