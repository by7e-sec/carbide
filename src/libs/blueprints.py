from glob import glob
from .blueprint import Blueprint

class Blueprints:
    def __init__(self, conf) -> None:
        pass

    def __parse(self):
        pass

    def __list(self):
        pass

    def list_available(self) -> list:
        pass

    def list_all(self) -> list:
        pass

    def get_blueprint(self, name) -> Blueprint:
        return Blueprint(name)
