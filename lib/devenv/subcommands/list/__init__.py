import logging
import devenv.configuration
from devenv.subcommands.base_command import Command

logger = logging.getLogger('devenv.subcommands.edit')

list_parser = None

def add_subparser(subparsers):
    list_parser = subparsers.add_parser("list")
    devenv.configuration.add_default_parser_options(list_parser)

class List(Command):
    def __init__(self, args, configs):
        super().__init__(args, configs)
        devenv.configuration.set_logging_attrs(args, logger)

    def run(self):
        for cfg in self.configs.keys():
            print(cfg)
