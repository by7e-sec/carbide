import paramiko
from .blueprints import Blueprints

class Processor:
    blueprints: None

    def __init__(self, conf: dict, opts: str) -> None:
        self.blueprints = Blueprints(conf)

    def run(self):
        print('running!')
