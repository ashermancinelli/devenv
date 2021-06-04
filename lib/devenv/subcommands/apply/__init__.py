import logging
import os
import argparse
from devenv.subcommands.base_command import Command
import devenv.configuration
import devenv.generators

apply_parser = None

def add_subparser(subparsers):
    apply_parser = subparsers.add_parser("apply")
    apply_parser.add_argument('--export', '-e', type=str,
        help='Environment variables to set in target environment of the form \n'
        '--export var1=var,var2 where var1 is set to "var", and var2 is set to\n'
        'the value of var2 in host environment.', default=None)
    apply_parser.add_argument('name', type=str, help='Name of configuration to be applied.')
    devenv.configuration.add_default_parser_options(apply_parser)

class Apply(Command):

    def __init__(self, args, configs):
        super().__init__(args, configs)

    def run(self):
        print(f'Loading environment {self.args.name}')
        cmd = devenv.generators.generate_script(self.args, self.configs[self.args.name])

        if self.args.debug:
            print(cmd)
        else:
            logging.info('Running command for environment {self.args.name}')
            os.system(cmd)
