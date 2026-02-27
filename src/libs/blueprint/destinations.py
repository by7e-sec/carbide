from typing import Any, Generator

from ..config import Config
from .destination import Destination


class Destinations:
    """
    Process destination items
    """

    destinations: list[dict[str, Any]] = []
    conf: Config

    def __init__(self, dests: list[dict[str, Any]], conf: Config) -> None:
        self.destinations = dests
        self.conf = conf

    def __iter__(self) -> Generator[Destination, Any, None]:
        for dest in self.destinations:
            yield Destination(dest, self.conf)
