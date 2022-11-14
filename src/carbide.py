#!/usr/bin/env python3

from optparse import OptionParser
from libs.config import Config
from libs.processor import Processor

parser = OptionParser()
parser.add_option("-c", "--config", dest="config", default="",
                  help="Path to config file")
parser.add_option("-b", "--blueprint", dest="blueprint", action="append",
                  default=[], help="Run specific blueprint (stackable)")
parser.add_option("-l", "--list", action="store_true", dest="listblueprints",
                  default=False, help="List available blueprints")

(opts, args) = parser.parse_args()

if __name__ == "__main__":
    conf = Config(opts.config)
    proc = Processor(conf, opts)

    proc.run()
