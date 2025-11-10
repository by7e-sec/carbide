from .destination import Destination


class Destinations:
    """
    Process destination items
    """

    destinations = []

    def __init__(self, dests: list) -> None:
        self.destinations = dests

    def __iter__(self):
        for dest in self.destinations:
            yield Destination(dest)
