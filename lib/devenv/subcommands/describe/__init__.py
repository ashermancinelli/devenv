from typing import Dict
import logging
import pprint
pp = pprint.PrettyPrinter(indent=4)
from devenv.subcommands.base_command import Command
import devenv.configuration

logger = logging.getLogger('devenv.subcommands.describe')

describe_parser = None

def add_subparser(subparsers):
    describe_parser = subparsers.add_parser("describe")
    describe_parser.add_argument('name', type=str, help='Name of configuration to be applied.')
    devenv.configuration.add_default_parser_options(describe_parser)

class Describe(Command):
    def __init__(self, args, configs):
        super().__init__(args, configs)
        devenv.configuration.set_logging_attrs(args, logger)

    def run(self):
        logger.info('Dumping configuration for environment "{self.args.name}"')
        pp.pprint(self.configs[self.args.name])
