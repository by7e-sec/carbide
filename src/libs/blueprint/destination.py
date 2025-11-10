from functools import partial


class Destination:
    destination: dict = {}

    def __init__(self, destination):
        self.destination = destination

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
