import os

import paramiko
from loguru import logger


class SftpAgent:
    auth: dict = {}
    client: paramiko.SSHClient = None

    def __init__(self):
        self.auth = {
            "hostname": "localhost",
            "port": 22,
            "username": None,
            "password": None,
            "pkey": None,
            "key_filename": None,
        }
        self.client = None

    def authenticate(self, auth: dict):
        try:
            client = paramiko.SSHClient()
            client.load_system_host_keys()
            client.set_missing_host_key_policy(paramiko.AutoAddPolicy())
            client.connect(**auth)

            self.client = client
        except paramiko.AuthenticationException as e:
            logger.warning(f"Authentication for machine {e} failed!")

    def copy_files(self, files: list, dest_folder: str):
        scp = paramiko.SFTPClient.from_transport(self.client.get_transport())
        logger.debug(f"Creating {dest_folder} on remote machine.")
        try:
            scp.mkdir(dest_folder)
        except OSError:
            pass

        for file in files:
            dst_file = os.path.join(dest_folder, file[1])
            logger.debug(f"Transfering file {file[0]} to {dest_folder}/{file[1]}")
            if os.path.isdir(file[0]):
                try:
                    scp.mkdir(dst_file)
                except OSError:
                    pass
            else:
                scp.put(file[0], dst_file)

        logger.debug("Done.")
