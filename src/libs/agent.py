from loguru import logger


class Agent:
    auth: dict = {}
    client: None

    def __init__(self):
        self.auth: dict = {}
        self.client = None

    def authenticate(self, auth: dict):
        logger.warning("`authenticate` should be properly initialized!")

    def copy_files(self, files: list, dest_folder: str):
        logger.warning("`copy_files` should be properly initialized")
