from .blueprints import Blueprints
from .config import Config
from .fsutils import Local
from colorama import Fore, Style
import sys


class Processor:
    blueprints: Blueprints
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
        rst = Style.RESET_ALL

        bps = self.blueprints.list_all()
        print(Style.BRIGHT + Fore.MAGENTA + "Available blueprints:")
        for bp in bps:
            is_valid = bright_green + 'Valid' if bps[bp]['valid'] else dim_red + 'Not valid'
            is_active = bright_green + 'Active' if bps[bp]['active'] else dim_red + 'Inactive'
            print(Style.BRIGHT + Fore.YELLOW + bp + ': ' + is_valid + Fore.WHITE + ' || ' + is_active + rst)
            if bps[bp]['description'] != '':
                print(Style.DIM + Fore.WHITE + ' # ' + Fore.MAGENTA + bps[bp]['description'])
            else:
                print(Style.DIM + Fore.WHITE + ' # No description')

            print(Style.RESET_ALL)

        sys.exit(0)

    def run(self):
        for bp in self.blueprints.get_blueprints():
            cp_local = Local(bp)
            cp_local.deploy()
