from functools import partial

from ..config import Config


class Destination:
    destination: dict = {}
    conf: Config

    def __init__(self, destination, conf: Config):
        self.destination: dict = destination
        self.conf: Config = conf

    def __getattr__(self, name):
        """
        Set get_ methods for coresponding dictionary names
        """
        if name.startswith("get_") and name != "get_authenticate":
            x = lambda a: self.destination[a]
            return partial(x, name[4:])
        else:
            raise AttributeError

    def auth(self):
        return self.destination["authenticate"]

    def is_local(self):
        return self.destination["local"] if "local" in self.destination else False

    def is_valid(self):
        return bool(self.conf.get_machine(self.destination["machine"]))

    def show_destination_error(self):
        if not self.conf.get_machine(self.destination["machine"]):
            return "Destination not listed in configuration!"
