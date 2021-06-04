import logging
import os
import argparse
from devenv.subcommands.base_command import Command
import devenv.configuration
import devenv.generators

logger = logging.getLogger('devenv.subcommands.status')

status_parser = None

def add_subparser(subparsers):
    status_parser = subparsers.add_parser("status")
    devenv.configuration.add_default_parser_options(status_parser)

class Status(Command):

    def __init__(self, args, configs):
        super().__init__(args, configs)
        devenv.configuration.set_logging_attrs(args, logger)

    def run(self):
        env = os.environ.get('DEVENV_ENV_NAME', 'None')
        layers = os.environ.get('DEVENV_LAYERS', '0')
        print(f'Active Environment: {env}')
        print(f'Devenv Layers: {layers}')
