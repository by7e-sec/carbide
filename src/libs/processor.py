from .blueprints import Blueprints
from .config import Config
# from .deputils import Local, Remote
from colorama import Fore, Style
import sys


class Processor:
    blueprints: None
    opts: dict

    def __init__(self, conf: Config, opts: dict) -> None:
        self.blueprints = Blueprints(conf)
        self.opts = opts

        if self.opts.listblueprints:
            self.list_blueprints()

    def list_blueprints(self):
        # Colors
        bright_green = Style.BRIGHT + Fore.GREEN
        dim_red = Style.DIM + Fore.RED

        bps = self.blueprints.list_all()
        print(Style.BRIGHT + Fore.MAGENTA + "Available blueprints:")
        for bp in bps:
            is_valid = bright_green + 'Valid' if bps[bp]['valid'] else dim_red + 'Not valid'
            is_active = bright_green + 'Active' if bps[bp]['active'] else dim_red + 'Inactive'
            print(Style.BRIGHT + Fore.YELLOW + bp + ': ' + is_valid + Fore.WHITE + ' || ' + is_active)
            if 'description' in bps[bp]:
                print(Style.DIM + Fore.WHITE + ' >> ' + bps[bp]['description'])

            print(Style.RESET_ALL)

        sys.exit(0)

    def run(self):
        pass
