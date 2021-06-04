import logging
import subprocess
import os
import devenv.utils
from devenv.subcommands.base_command import Command

logger = logging.getLogger('devenv.subcommands.edit')

version_parser = None

def add_subparser(subparsers):
    version_parser = subparsers.add_parser("version", add_help=False)
    devenv.utils.add_default_parser_options(version_parser)

class Version(Command):
    def __init__(self, args, config):
        super().__init__(args, config)
        devenv.utils.set_logging_attrs(args, logger)

    def run(self):
        label = subprocess.check_output(["git", "describe", "--tags"],
                cwd=self.config['definitions']['devenv']).strip().decode()
        logger.debug(f'Got description "{label}" from "git describe --tags"')
        version = f'devenv {label}'
        print(version)

