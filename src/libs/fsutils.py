import os
import shutil
from loguru import logger
from .blueprint import Blueprint


class Local:
    bp: Blueprint = None

    def __init__(self, bp: Blueprint) -> None:
        print(bp)

    def deploy(src: str, dst: str):
        try:
            os.chdir(src)
            for (root, _, files) in os.walk(src, topdown=True):
                os.makedirs(f'{root}')
                for f in files:
                    logger.debug(f"Copy: {root}/{f} to {dst}/{f}")
                    shutil.copy(f'{root}/{f}', f'{dst}/{f}')
        except Exception as e:
            logger.critical(f"Unable to copy data to destination!\n{e}")


class Remote:
    def __init__(self) -> None:
        pass
