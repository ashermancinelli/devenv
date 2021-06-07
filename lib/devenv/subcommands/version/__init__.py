import logging
import subprocess
import os
from typing import Dict
import devenv.utils
from devenv.subcommands.base_command import Command
import pprint
pp = pprint.PrettyPrinter(indent=4)
import json

logger = logging.getLogger('devenv.subcommands.version')

version_parser = None

def add_subparser(subparsers):
    version_parser = subparsers.add_parser("version", add_help=False)
    devenv.utils.add_default_parser_options(version_parser)

class Version(Command):
    def __init__(self, args, config):
        super().__init__(args, config)

    def run(self, do_print=True) -> Dict[str, str]:
        git_description = subprocess.check_output(["git", "describe", "--tags"],
                cwd=self.config['definitions']['devenv']).strip().decode()
        logger.debug(f'Got description "{git_description}" from "git describe --tags"')

        version_info = devenv.utils.make_version_info(git_description)

        if do_print:
            if self.args.verbose or self.args.debug:
                print(json.dumps(version_info, indent=4))
            else:
                print('devenv %s' % version_info.label)

        return version_info
