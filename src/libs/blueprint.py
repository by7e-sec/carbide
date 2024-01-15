import os
import tempfile

from loguru import logger

from libs.config import Config


class Blueprint:
    """
    Blueprint
    """

    name: str = ""
    bp: dict = {}
    valid: bool = False
    tmp_folder: str
    conf: Config

    def __init__(self, filename: str, data: dict, conf: Config) -> None:
        self.name: str = os.path.splitext(filename)[0]
        self.conf: Config = conf
        self.tmp_folder = ""
        self.bp: dict = data

        # Check for validity of blueprint if it contains needed components
        self.__check_valid()

        # Misc postprocessing
        self.__postprocessing()

    def __check_valid(self) -> None:
        """
        Check validity of a blueprint
        """
        if "blueprint" not in self.bp:
            logger.error("Blueprint is not wrapped in `blueprint` structure!")
            return

        if "kind" not in self.bp["blueprint"]:
            logger.error("Kind is missing from the blueprint!")
            return

        if self.bp["blueprint"]["kind"] not in ["sftp", "local"]:
            logger.error("Invalid kind of transport specified in blueprint!")
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

    def __postprocessing(self):
        """
        Misc. blueprint postprocessing
        """
        if self.valid:
            # Bind authentication to a machine blueprint from master config file if available
            for dest in self.bp["blueprint"]["deploy"]["destinations"]:
                dest.update(self.conf.get_machine(dest["machine"]))

    def get_auth_dict(self, auth_name: str, machine: str) -> bool:
        auth = self.conf.get_auth(auth_name)
        auth.update(self.conf.get_machine(machine))

        if "error" in auth:
            self.valid = False
            return {}

        auth_out = {}
        for key in ["username", "password", "hostname", "port"]:
            if key in auth:
                auth_out.update({key: auth[key]})

        return auth_out

    def is_active(self) -> bool:
        """
        Clieck if a blueprint is active. It can be disabled with
        'active: false' directive in the blueprint

        Returns:
            bool Is blueprint active
        """
        if not self.valid:
            return False

        if "active" not in self.bp["blueprint"]:
            return True

        return self.bp["blueprint"]["active"]

    def is_valid(self) -> bool:
        """
        Is blueprint even valid?

        Return
            bool Validity of the blueprint as checked by __check_valid
        """
        return self.valid

    def set_config(self, conf: Config) -> None:
        """
        Set instance of config file. Usually it's set automatically
        """
        self.conf = conf

    def set_temp(self, tmp: str) -> None:
        """
        Set temporary folder for some operations
        """
        self.tmp_folder = tmp

    def get_name(self) -> str:
        """
        Get blueprint (file) name

        Returns
            str Blueprint filename with stipped paths and file extension
        """
        return self.name

    def get_description(self) -> str:
        """
        Get optional blueprint description

        Returns
            str Blueprint optional description or empty string if the blueprint isn't valid
        """
        if not self.valid or "description" not in self.bp["blueprint"]:
            return ""

        return self.bp["blueprint"]["description"].strip()

    def get_kind(self) -> str:
        """
        Get kind of a blueprint. Current supported types:
         - sftp

        Returns:
            bool Is blueprint active
        """
        if not self.valid:
            return ""

        if "kind" not in self.bp["blueprint"]:
            return "sftp"

        return self.bp["blueprint"]["kind"]

    def get_temp(self) -> str:
        """
        Get temporary folder if one is set or create a new one

        Returns
            str Temporary folder path
        """
        if self.tmp_folder == "":
            self.tmp_folder = tempfile.mkdtemp()

        return self.tmp_folder

    def is_source_local(self) -> bool:
        """
        Checks if source machine is local

        Returns
            bool
        """
        machine = self.bp["blueprint"]["deploy"]["source"]["machine"]
        data = self.conf.get_machine(machine)

        return data["local"]

    def get_source(self) -> str:
        """
        Get source folder

        Returns
            str Source folder or empty string if the blueprint isn't valid
        """
        if not self.valid:
            return ""

        return self.bp["blueprint"]["deploy"]["source"]

    def get_destinatons(self) -> list:
        """
        Get list of destinations

        Returns
            list List of destination or empty list of the blueprint isn't valid
        """
        if not self.valid:
            return []

        return self.bp["blueprint"]["deploy"]["destinations"]
