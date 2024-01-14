import paramiko
from loguru import logger


class Scp:
    auth = {"server": "localhost", "port": 22, "user": None, "pass": None, "key": None, "keypass": None}
    client = None

    def __init__(self, auth: dict):
        self.auth = self.auth.update(auth)

    def authenticate(self):
        try:
            client = paramiko.SSHClient()
            client.load_system_host_keys()
            client.set_missing_host_key_policy(paramiko.AutoAddPolicy())
            client.connect(self.auth["server"], self.auth["port"], self.auth["user"], self.auth["password"])

            self.client = client
        except paramiko.AuthenticationException as e:
            logger.warning(f"Authentication for machine {e} is not in global config file!")

    def copy(self, files: list):
        scp = paramiko.SFTPClient(self.client.get_transport())
        for file in files:
            scp.put(file[0], file[1])
