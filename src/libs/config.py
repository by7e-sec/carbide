import os
import sys

import yaml
from loguru import logger

default_paths = [
    "/etc/carbide/carbide.yaml",
    "~/.local/share/carbide/carbide.yaml",
    "~/.carbide/carbide.yaml",
    "../config/carbide.yaml",
    "./config/carbide.yaml",
    "./carbide.yaml",
]


class Config:
    conf = {}

    def __init__(self, cfgpath: str = "") -> None:
        """
        Scan for default locations if no path is provided else attempt to load config file directly
        """
        if cfgpath == "":
            self.__scan_default_paths()
        else:
            self.__load_config(cfgpath)

        # Init logging
        self.__init_logging()

    def __init_logging(self) -> None:
        """
        Setup app-wide logging
        """
        if "logging" in self.conf:
            if "file" in self.conf["logging"]:
                if "file_format" in self.conf["logging"]:
                    ff = self.conf["logging"]["file_format"]
                else:
                    ff = "{time} {level} {message}"

                logger.add(self.conf["logging"]["file"], colorize=True, format=ff)

            if "stdout_format" in self.conf["logging"]:
                ff = self.conf["logging"]["stdout_format"]
            else:
                ff = "<green>{time}</green> <level>{message}</level>"

            logger.add(sys.stdout, colorize=True, format=ff)

    def __load_config(self, file) -> None:
        """
        Attempt to blindly but safely load YAML file...
        """
        try:
            with open(file, "r") as f:
                self.conf = yaml.safe_load(f)
        except Exception as e:
            logger.error(f"Cannot read YAML file!\n{e}")

    def __scan_default_paths(self) -> None:
        """
        Scan default paths if the path to file isn't provided
        """
        for file in default_paths:
            file = os.path.expanduser(file)
            if os.path.exists(file):
                print(f"Config found in {file}. Loading...")
                self.__load_config(file)

                return

        logger.error("Cannot locate carbide.yaml in default locations! Giving up.")
        sys.exit(1)

    def get_blueprints_location(self) -> str:
        """
        Get path to blueprints from config file

        Returns
            str Blueprints folder
        """
        bp_folder = self.conf["blueprints"] if "blueprints" in self.conf else ""

        if not os.path.exists(bp_folder) or bp_folder == "":
            logger.error(f"Blueprint folder '{bp_folder}' doesn't exist!")
            sys.exit(1)

        return bp_folder

    def get_machine(self, machine: str) -> dict:
        """
        Get machine details

        Returns
            dict {local, {host, port, authentication}}
        """
        if "machines" in self.conf and type(self.conf["machines"]) == dict:
            return self.conf["machines"][machine] if machine in self.conf["machines"] else {}
        return {}

    def get_auth(self, machine) -> dict:
        """
        Gets authentication for a machine from global config file

        Returns
            dict {local, {host, port, authentication}}
        """
        if machine in self.conf["authentication"]:
            return self.conf["authentication"][machine]
        elif machine == "local":
            return {"local": True}

        logger.warning(f"Authentication for machine {machine} is not in global config file!")
        return {}
