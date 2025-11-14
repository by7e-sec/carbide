from abc import ABC, abstractmethod

from loguru import logger


class Agent(ABC):
    auth: dict = {}
    client: None

    def __init__(self):
        self.auth: dict = {}
        self.client = None

    @abstractmethod
    def authenticate(self, auth: dict):
        logger.warning("`authenticate` should be properly initialized!")

    @abstractmethod
    def copy_files(self, files: list, dest_folder: str, remote_machine: str):
        logger.warning("`copy_files` should be properly initialized")
