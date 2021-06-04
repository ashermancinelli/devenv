import os
import logging
import shutil
from devenv.subcommands.base_command import Command
import devenv.utils

logger = logging.getLogger('devenv.subcommands.edit')

edit_parser = None


def add_subparser(subparsers):
    edit_parser = subparsers.add_parser("edit")
    devenv.utils.add_default_parser_options(edit_parser)


class Edit(Command):
    def __init__(self, args, configs):
        super().__init__(args, configs)
        devenv.utils.set_logging_attrs(args, logger)

    def get_default_editor(self) -> str:
        logger.debug('Searching for default editor')
        editor = None
        default_editors = [
                os.environ.get('DEVENV_EDITOR', ''),
                os.environ.get('EDITOR', ''),
                'vim',
                'vi',
                'emacs',
                'nano',
                'ed'
                ]
        for ed in default_editors:
            logger.debug(f'Looking for editor "{ed}"')
            if not editor is None:
                break
            editor = shutil.which(ed)

        if editor is None:
            raise RuntimeError('Could not find valid editor! '
                    'Please set environment variable "DEVENV_EDITOR" or "EDITOR"')

        logger.info(f'Using editor "{editor}"')
        return editor

    def run(self):
        editor = self.get_default_editor()
        os.system(f'{editor} {self.args.config_file}')
