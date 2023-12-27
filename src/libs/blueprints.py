import os
from glob import glob
from typing import List

import yaml
from loguru import logger

from .blueprint import Blueprint
from .config import Config


class Blueprints:
    bps: List[Blueprint] = []
    conf: Config

    def __init__(self, conf: Config) -> None:
        self.conf = conf
        loc: str = conf.get_blueprints_location()
        if loc != "" and os.path.exists(os.path.expanduser(loc)):
            self.__list(loc)
        else:
            logger.error(f"Blueprints path {loc} is unreachable!")

    def __list(self, loc: str) -> None:
        blueprints: List[str] = glob(os.path.join(loc, "*.yaml"))
        for blueprint in blueprints:
            try:
                with open(blueprint) as bp:
                    data: dict = yaml.safe_load(bp)
                    self.bps.append(Blueprint(os.path.basename(blueprint), data, self.conf))
            except Exception as e:
                logger.warning(f"You have an error in blueprint {blueprint}:\n{str(e)}")

    def list_all(self) -> dict:
        out = {}
        for bp in self.bps:
            out[bp.get_name()] = {
                "active": bp.is_active(),
                "valid": bp.is_valid(),
                "kind": bp.get_kind(),
                "description": bp.get_description(),
            }

        return out

    def get_blueprints(self, names: list):
        bp_names = [bp.get_name() for bp in self.bps]
        if not names:  # Return all blueprints if nothing was specified
            return self.bps
        else:
            out = []
            for name in names:
                if not name in bp_names:
                    logger.error(f"{name} is not in a list of valid blueprint names!")
                else:
                    logger.debug(f"Added {name} to the pool")
                    bp = [bp for bp in self.bps if bp.get_name() == name]
                    out.extend(bp)
        return out
