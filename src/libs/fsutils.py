import os
import shutil
from loguru import logger
from .blueprint import Blueprint


class Local:
    bp: Blueprint = None

    def __init__(self, bp: Blueprint) -> None:
        self.bp = bp  # Load blueprint

    def deploy(self):
        src = self.bp.get_source()
        if 'folder' in src:
            stype = 'folder'
            ssource = src['folder']
        elif 'items' in src:
            stype = 'items'
            ssource = src['items']

        if stype == 'folder':
            try:
                source_files = []
                for (root, _, files) in os.walk(ssource, topdown=True):
                    pth = root.replace(ssource, '')
                    filtered = False
                    if 'filter' in src:
                        for filter in src['filter']:
                            if filter in pth:
                                filtered = True

                    if not filtered:
                        source_files.append(root)
                        for file in files:
                            source_files.append(os.path.join(root, file))

                destinations = self.bp.get_destinatons()
                for dst in destinations:
                    if not os.path.exists(dst['folder']):
                        os.mkdir(dst['folder'])

                    for sf in source_files:
                        destfile = os.path.join(dst['folder'], sf.replace(ssource, ''))
                        if os.path.isdir(sf) and not os.path.exists(destfile):
                            os.makedirs(destfile)
                            logger.debug(f"Creating folder {destfile}")
                        elif not os.path.isdir(sf):
                            shutil.copyfile(sf, destfile)
                            logger.debug(f"Copy {sf} to {destfile}")

            except Exception as e:
                logger.critical(f"Unable to copy data to destination!\n{e}")


class Remote:
    def __init__(self) -> None:
        pass
