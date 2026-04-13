#!/usr/bin/env python3

from argparse import ArgumentParser

from libs import agents_registry
from libs.config import Config
from libs.processor import Processor

agents_registry.discover_agents("agents")

parser = ArgumentParser()
parser.add_argument("-c", "--config", dest="config", default="", help="Path to config file")
parser.add_argument("-b", "--blueprint", dest="blueprint", action="append", default=[], help="Run specific blueprint (stackable)")
parser.add_argument(
    "-l", "--list", action="store_true", dest="listblueprints", default=False, help="List available blueprints and exit"
)
parser.add_argument(
    "-g", "--capabilities", action="store_true", dest="listcapabilities", default=False, help="List Tlisk's capabilities and exit"
)

opts = parser.parse_args()
conf = Config(opts.config)

# instance the processor
proc = Processor(conf, opts)

if __name__ == "__main__":
    proc.run()
