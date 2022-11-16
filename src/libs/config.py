import os
import sys
import yaml
from loguru import logger

default_paths = [
    '/etc/carbide/carbide.yaml',
    '~/.local/carbide/carbide.yaml',
    '../config/carbide.yaml',
    './config/carbide.yaml',
    './carbide.yaml',
]


class Config:
    conf = {}

    def __init__(self, cfgpath: str = '') -> None:
        # Scan for default locations if no path is provided
        # else attempt to load config file directly
        if cfgpath == '':
            self.__scan_default_paths()
        else:
            self.__load_config(cfgpath)

        # Init logging
        self.__init_logging()

    def __init_logging(self):
        if 'logging' in self.conf:
            if 'file' in self.conf['logging']:
                if 'file_format' in self.conf['logging']:
                    ff = self.conf['logging']['file_format']
                else:
                    ff = "{time} {level} {message}"

                logger.add(self.conf['logging']['file'], colorize=True, format=ff)

            if 'stdout_format' in self.conf['logging']:
                ff = self.conf['logging']['stdout_format']
            else:
                ff = "<green>{time}</green> <level>{message}</level>"

            logger.add(sys.stdout, colorize=True, format=ff)

    def __load_config(self, file) -> None:
        # Attempt to blindly but safely load YAML file...
        try:
            with open(file, 'r') as f:
                self.conf = yaml.safe_load(f)
        except Exception:
            logger.error("Cannot read YAML file!")

    def __scan_default_paths(self) -> None:
        # Scan default path for a potential config file.
        for file in default_paths:
            if os.path.exists(os.path.expanduser(file)):
                print(f"Config found in {file}. Loading...")
                self.__load_config(file)

                return

        logger.error("Cannot locate carbide.yaml in default locations! Giving up.")
        sys.exit(1)

    def get_blueprints_location(self) -> str:
        # Return the path provided in the main config file
        bp_folder = self.conf['blueprints'] if 'blueprints' in self.conf else ''

        return bp_folder
