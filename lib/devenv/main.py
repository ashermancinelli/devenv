import yaml
import sys
import argparse
import os
from typing import Dict
import logging
import pprint
pp = pprint.PrettyPrinter(indent=4)

import devenv
import devenv.subcommands
import devenv.configuration
import devenv.defaults as defaults
import devenv.generators as generators
from devenv.configuration import check_config_file, merge_config_file
from devenv.defaults import configs, aliases

logger = logging.getLogger('devenv.main')

# See https://stackoverflow.com/questions/20094215/argparse-subparser-monolithic-help-output
class _HelpAction(argparse._HelpAction):

    def __call__(self, parser, namespace, values, option_string=None):
        parser.print_help()

        # retrieve subparsers from parser
        subparsers_actions = [
            action for action in parser._actions
            if isinstance(action, argparse._SubParsersAction)]
        # there will probably only be one subparser_action,
        # but better save than sorry
        for subparsers_action in subparsers_actions:
            # get all subparsers and print help
            for choice, subparser in subparsers_action.choices.items():
                print('-' * 80)
                print("\nHelp for subcommand '{}'".format(choice))
                print('-' * 30)
                print(subparser.format_help())
            print('-' * 80)

        parser.exit()

def main():
    parser = argparse.ArgumentParser(
            description='Configure development environment based on predetermined configurations',
            formatter_class=argparse.RawTextHelpFormatter,
            add_help=False)
    parser.add_argument('--config-file', '-c', type=str,
            help=f'Path to configuration file. Defaults to {defaults.config_locations[0]}',
            default=os.path.expanduser(defaults.config_locations[0]))
    parser.add_argument('--help', '-h', help='View all program options', action=_HelpAction)
    devenv.configuration.add_default_parser_options(parser)
    subparsers = parser.add_subparsers(help='sub-command --help', dest='command')
    devenv.subcommands.add_subparsers(subparsers)
    devenv.configuration.apply_shorthand_commands(sys.argv)
    args = parser.parse_args()

    # retrieve subparsers from parser
    subparsers_actions = [
        action for action in parser._actions
        if isinstance(action, argparse._SubParsersAction)]
    # there will probably only be one subparser_action,
    # but better safe than sorry
    for subparsers_action in subparsers_actions:
        # get all subparsers and print help
        for choice, subparser in subparsers_action.choices.items():
            print("Subparser '{}'".format(choice))
            print(subparser.format_help())

    devenv.configuration.set_logging_attrs(args, logger)

    logger.debug(f'Got args: {args}')

    check_config_file(args)

    merge_config_file(configs, aliases, args)

    for k, v in aliases.items():
        logger.debug(f'Adding alias "{k}" = "{v}"')
        configs[k] = configs[v]

    devenv.subcommands.handle_subcommand(args, configs)
    return 0
