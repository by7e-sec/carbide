import sys

from colorama import Fore, Style
from loguru import logger

from .blueprints import Blueprints
from .config import Config
from .transport import Transport


class Processor:
    blueprints: Blueprints
    opts: dict
    conf: Config

    def __init__(self, conf: Config, opts: dict) -> None:
        self.opts = opts
        self.conf = conf
        self.blueprints = Blueprints(conf, [] if self.opts.listblueprints else self.opts.blueprint)

        if self.opts.listblueprints:
            self.list_blueprints()

    def list_blueprints(self) -> None:
        """
        Pretty display the list of blueprints by name, validity, activity, type,
        and description, and exit.
        """
        # Colors
        bright_green = Style.BRIGHT + Fore.GREEN
        dim_red = Style.DIM + Fore.RED

        bps = self.blueprints.list_all()
        print(Style.BRIGHT + Fore.MAGENTA + "Available blueprints:")
        for bp in bps:
            is_valid = bright_green + "Valid" if bps[bp]["valid"] else dim_red + "Not valid"
            is_active = bright_green + "Active" if bps[bp]["active"] else dim_red + "Inactive"
            is_valid = is_valid + Style.RESET_ALL
            is_active = is_active + Style.RESET_ALL

            print(Style.BRIGHT + Fore.YELLOW + bp + ": " + is_valid + Fore.WHITE + " || " + is_active)
            print(Style.BRIGHT + Fore.BLUE + " Kind: " + bps[bp]["kind"] if bps[bp]["kind"] else "fallback")
            if bps[bp]["description"] != "":
                print(Style.DIM + Fore.WHITE + " # " + Fore.MAGENTA + bps[bp]["description"])

            print(Style.RESET_ALL)

        sys.exit(0)

    def run(self) -> None:
        """
        Run blueprint
        """
        for bp in self.blueprints.get_blueprints():
            if bp.is_active():
                if bp.is_source_local():
                    try:
                        tx = Transport(bp)
                        for dest in bp.get_destinatons():
                            tx.authenticate(dest["authenticate"], dest["machine"])
                            if tx.is_client_active():
                                tx.copy_files(dest["folder"])
                            else:
                                logger.warning("Client has not been initiated! Skipping further processing!")
                    except PermissionError as pe:
                        logger.error(
                            f"There was a permission error while running the blueprint: {pe}. Do you need to be root?"
                        )
                    # except Exception as e:
                    #     logger.critical(f"There was an error executing the blueprint: {e}")
