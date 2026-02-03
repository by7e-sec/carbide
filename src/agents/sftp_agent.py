import os
import re
import time
from pathlib import Path

import paramiko
from loguru import logger

from libs.agent import Agent


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

    def copy_files(self, files: list, dest_folder: str, remote_machine: str) -> None:
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
                logger.debug(f"Symlinking {dst_file} => {symlink}")
                try:  # Remove remote symlink, otherwise we get a "failure"
                    scp.stat(f"{dst_file}")
                    scp.unlink(f"{dst_file}")
                except IOError:
                    pass

                scp.symlink(f"{symlink}", f"{dst_file}")
            else:
                logger.debug(f"Copying {file[0]} => {remote_machine}:{dest_folder}/{file[1]}")
                scp.put(file[0], dst_file)

        logger.debug("Done.")

    def run_commands(self, commands: list) -> None:
        """
        Execute remote commands
        """
        for cmd in commands:
            logger.debug(f"Executing remote command: {cmd}")
            _, stdout, stderr = self.client.exec_command(cmd)
            out = stdout.read().decode("utf-8")
            err = stderr.read().decode("utf-8")
            if err:
                logger.error(f"Remote error occured: {err}")
                logger.error(f"stdout was: {out}")
            time.sleep(0.1)
