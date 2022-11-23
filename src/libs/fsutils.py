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
            except Exception as e:
                logger.critical(f"Unable to copy data to destination!\n{e}")
        elif stype == 'items':
            source_files = ssource

        try:
            destinations = self.bp.get_destinatons()
            for dst in destinations:
                if not os.path.exists(dst['folder']):
                    os.mkdir(dst['folder'])

                for sf in source_files:
                    if not os.path.isdir(sf):
                        destfile = os.path.join(dst['folder'], sf.replace(ssource, ''))
                        if not os.path.exists(os.path.dirname(destfile)):
                            logger.debug(f"Creating folder {os.path.dirname(destfile)}")
                            os.makedirs(os.path.dirname(destfile))
                        shutil.copyfile(sf, destfile)
                        logger.debug(f"Copy {sf} to {destfile}")

        except Exception as e:
            logger.critical(f"Unable to copy data to destination!\n{e}")


class Remote:
    bp: Blueprint = None

    def __init__(self, bp: Blueprint) -> None:
        self.bp = bp  # Load blueprint
