import logging
import devenv.utils
from devenv.subcommands.base_command import Command

logger = logging.getLogger('devenv.subcommands.list')

list_parser = None

def add_subparser(subparsers):
    list_parser = subparsers.add_parser("list")
    devenv.utils.add_default_parser_options(list_parser)

class List(Command):
    def __init__(self, args, config):
        super().__init__(args, config)
        devenv.utils.set_logging_attrs(args, logger)

    def run(self):
        print('Environments:')
        for env in self.config['environments'].keys():
            print('  ', env)

        print()
        print('Aliases:')
        for alias in self.config['aliases'].keys():
            print('  ', alias, ' -> ', self.config['aliases'][alias])

