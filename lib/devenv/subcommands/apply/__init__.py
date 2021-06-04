import logging
import os
import argparse
from devenv.subcommands.base_command import Command
import devenv.utils
import devenv.generators

logger = logging.getLogger('devenv.subcommands.apply')

apply_parser = None

def add_subparser(subparsers):
    apply_parser = subparsers.add_parser("apply")
    apply_parser.add_argument('--export', '-e', type=str,
        help='Environment variables to set in target environment of the form \n'
        '--export var1=var,var2 where var1 is set to "var", and var2 is set to\n'
        'the value of var2 in host environment.', default=None)
    apply_parser.add_argument('name', type=str, help='Name of configuration to be applied.')
    devenv.utils.add_default_parser_options(apply_parser)

class Apply(Command):

    def __init__(self, args, config):
        super().__init__(args, config)
        devenv.utils.set_logging_attrs(args, logger)

    def run(self):
        logging.info(f'Creating commands for environment {self.args.name}')

        if self.args.name in self.config['aliases'].keys():
            logger.debug(f'Using alias "{self.args.name}" = "{config["aliases"][self.args.name]}"')
            self.args.name = config['aliases'][self.args.name]

        cmd = devenv.generators.generate_script(self.args, self.config['environments'][self.args.name])

        if self.args.debug:
            print(cmd)
        else:
            logger.info('Running command for environment {self.args.name}')
            os.system(cmd)
