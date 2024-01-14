import os

from loguru import logger

from .blueprint import Blueprint


class Transport:
    bp: Blueprint = None
    source_files: list = []

    def __init__(self, bp: Blueprint) -> None:
        self.bp = bp
        self.source_files = []

        self.__index_source_files()

        self.init_agent()

    def __index_source_files(self):
        src = self.bp.get_source()
        if src["type"] == "folder":
            try:
                source_files = []
                for root, _, files in os.walk(src["folder"], topdown=True):
                    pth = root.replace(src["folder"], "")
                    filtered = False
                    if "filter" in src:
                        for filter in src["filter"]:
                            if filter in pth:
                                filtered = True

                    if not filtered:
                        if root != src["folder"]:
                            source_files.append((root,))

                        for file in files:
                            path = os.path.join(root, file)
                            source_files.append(
                                (
                                    path,
                                    path[len(src["folder"]) :],
                                )
                            )
            except Exception as e:
                logger.critical(f"Unable to copy data to destination!\n{e}")

        self.source_files = source_files

    def init_agent(self):
        print(self.bp.get_kind())

    def copy_files(self):
        pass
