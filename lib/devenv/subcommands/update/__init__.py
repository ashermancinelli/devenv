import logging
from typing import Dict
import subprocess
import devenv.utils
import pprint
pp = pprint.PrettyPrinter(indent=4)
import json
from devenv.subcommands.base_command import Command
from devenv.subcommands.version import Version

logger = logging.getLogger('devenv.subcommands.update')

update_parser = None

def add_subparser(subparsers):
    update_parser = subparsers.add_parser("update")
    devenv.utils.add_default_parser_options(update_parser)

class Update(Command):
    def __init__(self, args, config):
        super().__init__(args, config)

    def run(self):
        version_info: Dict[str, str] = Version(self.args, self.config).run(do_print=False)

        if self.args.debug or self.args.verbose:
            print('Got initial version info:\n%s' % json.dumps(version_info, indent=4))
        else:
            print('Got initial version: "%s"' % version_info.tag)

        logger.debug('Fetching from remote')
        subprocess.check_output(['git', 'fetch', '--all'],
                cwd=self.config['definitions']['devenv'])

        logger.debug('Checking for new commits to master')
        git_description = subprocess.check_output(['git', 'describe', '--tags', 'master'],
                cwd=self.config['definitions']['devenv']).strip().decode()

        new_version_info = devenv.utils.make_version_info(git_description)

        if self.args.debug or self.args.verbose:
            print('Got newest version info:\n%s' % json.dumps(new_version_info, indent=4))
        else:
            print('Got newest version: "%s"' % new_version_info.tag)

        if version_info.commit == new_version_info.commit:
            print('Nothing to do!')
        else:
            logger.debug('Updating to newest master')
            subprocess.check_output(['git', 'pull', 'origin', 'master', '--rebase'],
                    cwd=self.config['definitions']['devenv'])


