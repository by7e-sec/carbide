import logging
import os
import re
from pathlib import Path

import paramiko
from loguru import logger

from libs.agent import Agent

logging.basicConfig()
logging.getLogger("paramiko").setLevel(logging.DEBUG)  # for example


class SftpAgent(Agent):
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

    def copy_files(self, files: list, dest_folder: str, remote_machine: str):
        dest_folder = dest_folder.rstrip("/")
        scp = paramiko.SFTPClient.from_transport(self.client.get_transport())
        try:
            scp.mkdir(dest_folder)
            logger.debug(f"Creating {dest_folder} on {remote_machine}.")
        except OSError:
            pass

        for file in files:
            dst_file = os.path.join(dest_folder, file[1])
            if os.path.isdir(file[0]):
                try:
                    scp.mkdir(dst_file)
                except OSError:
                    pass
            elif os.path.islink(file[0]):
                src_dir = file[0][: 0 - len(file[1])]
                link_to = str(Path(file[0]).readlink())
                symlink = re.sub(r"^" + repr(src_dir)[1:-1], "", link_to)
                logger.debug(f"Symlinking {dst_file} => {dest_folder}/{symlink}")
                try:  # Remove remote symlink, otherwise we get a "failure"
                    scp.stat(f"{dest_folder}/{symlink}")
                    scp.unlink(f"{dest_folder}/{symlink}")
                except IOError:
                    pass

                scp.symlink(f"{dst_file}", f"{dest_folder}/{symlink}")
            else:
                logger.debug(f"Copying {file[0]} => {remote_machine}:{dest_folder}/{file[1]}")
                scp.put(file[0], dst_file)

        logger.debug("Done.")
