import os
from glob import glob
from typing import List

import yaml
from loguru import logger

from .blueprint import Blueprint


class Blueprints:
    bps: List[Blueprint] = []

    def __init__(self, conf) -> None:
        loc: str = conf.get_blueprints_location()
        if loc != "" and os.path.exists(os.path.expanduser(loc)):
            self.__list(loc)
        else:
            logger.error(f"Blueprints path {loc} is unreachable!")

    def __list(self, loc: str) -> None:
        confs: List[str] = glob(os.path.join(loc, "*.yaml"))
        for cfg in confs:
            try:
                with open(cfg) as f:
                    data: dict = yaml.safe_load(f)
                    self.bps.append(Blueprint(os.path.basename(cfg), data))
            except Exception as e:
                logger.warning(f"You have an error in blueprint {cfg}:\n{str(e)}")

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

    def get_blueprints(self):
        return self.bps
