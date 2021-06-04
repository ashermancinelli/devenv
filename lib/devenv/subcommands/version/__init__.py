import logging
import subprocess
import os
import devenv.configuration
from devenv.subcommands.base_command import Command

logger = logging.getLogger('devenv.subcommands.edit')

version_parser = None

def add_subparser(subparsers):
    version_parser = subparsers.add_parser("version", add_help=False)

class Version(Command):
    def __init__(self, args, configs):
        super().__init__(args, configs)
        devenv.configuration.set_logging_attrs(args, logger)

    def run(self):
        label = subprocess.check_output(["git", "describe", "--tags"],
                cwd=self.args.prefix).strip().decode()
        commit = subprocess.check_output(['git', 'show', '--oneline', '-s'],
                cwd=self.args.prefix).decode().strip().split(' ')[0]
        version = f'devenv {label}-{commit}'
        print(version)

