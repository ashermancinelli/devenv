from typing import Dict
import logging
import pprint
pp = pprint.PrettyPrinter(indent=4)
from devenv.subcommands.base_command import Command
import devenv.configuration

logger = logging.getLogger('devenv.subcommands.dump')

dump_parser = None

def add_subparser(subparsers):
    dump_parser = subparsers.add_parser("dump")
    devenv.configuration.add_default_parser_options(dump_parser)

class Dump(Command):
    def __init__(self, args, configs):
        super().__init__(args, configs)
        devenv.configuration.set_logging_attrs(args, logger)

    def run(self):
        logger.info('Dumping configurations')
        pp.pprint(self.configs)
