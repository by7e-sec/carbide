import os
from loguru import logger


class Blueprint:
    name: str = ''
    bp: dict = {}
    valid: bool = False

    def __init__(self, filename: str, data: dict) -> None:
        self.name: str = os.path.splitext(filename)[0]
        self.bp: dict = data

        self.__check_valid()

    def __check_valid(self):
        if 'blueprint' not in self.bp:
            logger.error('Blueprint is not wrapped in `blueprint` structure!')
            return

        if 'deploy' not in self.bp['blueprint']:
            logger.error('Deploy is missing from the blueprint!')
            return

        dep = self.bp['blueprint']['deploy']
        if 'source' not in dep:
            logger.error('`source` configuration is missing from the `deploy` section!')
            return

        if 'destination' not in dep and 'destinations' not in dep:
            logger.error('`destination(s)` configuration is missing from the `deploy` section!')
            return

        self.valid = True

    def is_active(self):
        if 'active' not in self.bp['blueprint']:
            return True

        return self.bp['blueprint']['active']

    def is_valid(self):
        if 'blueprint' not in self.bp or not self.valid:
            return False

        return True

    def get_host(self):
        pass

    def get_auth(self):
        pass

    def get_name(self) -> str:
        return self.name

    def get_description(self) -> str:
        if 'description' not in self.bp['blueprint']:
            return ''

        return self.bp['blueprint']['description']

    def get_source(self):
        if self.valid and 'source' in self.bp['blueprint']['deploy']:
            return self.bp['blueprint']['deploy']['source']

        return ''

    def get_destinatons(self):
        if 'destinations' not in self.bp['blueprint']:
            return ''
