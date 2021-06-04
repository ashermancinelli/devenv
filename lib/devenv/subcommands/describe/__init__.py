from typing import Dict
import logging
import pprint
pp = pprint.PrettyPrinter(indent=4)
from devenv.subcommands.base_command import Command
import devenv.utils

logger = logging.getLogger('devenv.subcommands.describe')

describe_parser = None

def add_subparser(subparsers):
    describe_parser = subparsers.add_parser("describe")
    describe_parser.add_argument('name', type=str, nargs='?', default=None,
            help='Name of environment to be described. If not supplied,'
            ' the entire configuration will be described.')
    devenv.utils.add_default_parser_options(describe_parser)

class Describe(Command):
    def __init__(self, args, config):
        super().__init__(args, config)
        devenv.utils.set_logging_attrs(self.args, logger)

    def run(self):
        if not self.args.name is None:
            logger.info('Dumping environment "{self.args.name}"')
            pp.pprint(self.config['environments'][self.args.name])
        else:
            logger.info('Dumping all environments')
            pp.pprint(self.config)
