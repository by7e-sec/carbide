import os


class Blueprint:
    name: str = ''
    bp: dict = {}

    def __init__(self, filename: str, data: dict) -> None:
        self.name: str = os.path.splitext(filename)[0]
        self.bp: dict = data

    def is_active(self):
        if 'active' not in self.bp['blueprint']:
            return True

        return self.bp['blueprint']['active']

    def is_valid(self):
        if 'blueprint' not in self.bp:
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
        pass

    def get_destinatons(self):
        pass
