from functools import partial

from ..config import Config


class Destination:
    destination: dict = {}
    conf: Config

    def __init__(self, destination: dict, conf: Config):
        self.destination = destination
        self.conf = conf

    def __getattr__(self, name):
        """
        Set get_ methods for coresponding dictionary names
        """
        if name.startswith("get_") and name != "get_authenticate":
            return partial(lambda a: self.destination[a], name[4:])
        else:
            raise AttributeError

    def auth(self):
        return self.destination["authenticate"]

    def is_local(self):
        return self.destination["local"] if "local" in self.destination else False

    def is_valid(self):
        return bool(self.conf.get_machine(self.destination["machine"]))

    def get_remote_commands(self, timing: str) -> dict:
        """
        Gathers the list of commands and scripts that might be executed before or after deployment
        """
        scripts = {"before": {"commands": [], "scripts": []}, "after": {"commands": [], "scripts": []}}

        for scr in scripts.keys():
            for exe in ["run-commands", "run-scripts"]:
                combo_str: str = f"{exe}-{scr}"
                destination_scripts = self.destination[combo_str] if combo_str in self.destination else []

                scripts[scr]["commands" if "commands" in combo_str else "scripts"].extend(destination_scripts)

        return scripts[timing]

    def show_destination_error(self):
        if not self.conf.get_machine(self.destination["machine"]):
            return "Destination not listed in configuration!"
