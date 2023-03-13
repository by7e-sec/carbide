import os
from loguru import logger
import tempfile
from libs.config import Config


class Blueprint:
    name: str = ""
    bp: dict = {}
    valid: bool = False
    tmp_folder: str
    conf: Config

    def __init__(self, filename: str, data: dict) -> None:
        self.name: str = os.path.splitext(filename)[0]
        self.bp: dict = data
        self.tmp_folder = ""
        self.conf: Config

        self.__check_valid()

    def __check_valid(self) -> None:
        if "blueprint" not in self.bp:
            logger.error("Blueprint is not wrapped in `blueprint` structure!")
            return

        if "deploy" not in self.bp["blueprint"]:
            logger.error("Deploy is missing from the blueprint!")
            return

        dep = self.bp["blueprint"]["deploy"]
        if "source" not in dep:
            logger.error("`source` configuration is missing from the `deploy` section!")
            return

        if "folder" not in dep["source"] and "items" not in dep["source"]:
            logger.error("`folder` or `items` not defined in `source`")
            return

        if "destinations" not in dep:
            logger.error("`destination` configuration is missing from the `deploy` section!")
            return

        self.valid = True

    def is_active(self) -> bool:
        if not self.valid:
            return False

        if "active" not in self.bp["blueprint"]:
            return True

        return self.bp["blueprint"]["active"]

    def is_valid(self) -> bool:
        return self.valid

    def set_config(self, conf: Config):
        self.conf = conf

    def set_temp(self, tmp: str):
        self.tmp_folder = tmp

    def get_name(self) -> str:
        return self.name

    def get_description(self) -> str:
        if not self.valid or "description" not in self.bp["blueprint"]:
            return ""

        return self.bp["blueprint"]["description"].strip()

    def get_temp(self):
        if self.tmp_folder == "":
            self.tmp_folder = tempfile.mkdtemp()

        return self.tmp_folder

    def is_source_local(self):
        machine = self.bp["blueprint"]["deploy"]["source"]["machine"]
        data = self.conf.get_machine(machine)
        return data["local"]

    def get_source(self) -> str:
        if not self.valid:
            return ""

        return self.bp["blueprint"]["deploy"]["source"]

    def get_destinatons(self) -> list:
        if not self.valid:
            return ""

        return self.bp["blueprint"]["deploy"]["destinations"]
