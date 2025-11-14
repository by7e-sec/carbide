from ..config import Config
from .destination import Destination


class Destinations:
    """
    Process destination items
    """

    destinations: list = []
    conf: Config

    def __init__(self, dests: list, conf: Config) -> None:
        self.destinations: list = dests
        self.conf: Config = conf

    def __iter__(self):
        for dest in self.destinations:
            yield Destination(dest, self.conf)
