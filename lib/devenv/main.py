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

def main():
    parser = argparse.ArgumentParser(
            description='Configure development environment based on predetermined configurations',
            formatter_class=argparse.RawTextHelpFormatter)
    parser.add_argument('--config-file', '-c', type=str,
            help=f'Path to configuration file. Defaults to {defaults.config_locations[0]}',
            default=os.path.expanduser(defaults.config_locations[0]))
    parser.add_argument('--full-help', help='Print extra long help information', action='store_true')
    devenv.configuration.add_default_parser_options(parser)
    subparsers = parser.add_subparsers(help='sub-command help', dest='command')
    devenv.subcommands.add_subparsers(subparsers)
    devenv.configuration.apply_shorthand_commands(sys.argv)
    args = parser.parse_args()

    if args.full_help:
        print(defaults.extra_help)
        sys.exit(0)

    devenv.configuration.set_logging_attrs(args, logger)

    logger.debug(f'Got args: {args}')

    check_config_file(args)

    merge_config_file(configs, aliases, args)

    for k, v in aliases.items():
        logger.debug(f'Adding alias "{k}" = "{v}"')
        configs[k] = configs[v]

    devenv.subcommands.handle_subcommand(args, configs)
    return 0
