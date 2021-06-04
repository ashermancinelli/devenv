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
import devenv.utils
import devenv.generators as generators

logger = logging.getLogger('devenv.main')
# logger.setLevel(logging.DEBUG)

def main(devenv_prefix):

    # Create configuration for devenv to use globally
    devenv_configuration = {
            'environments': dict(),
            'aliases': dict(),
            'command-aliases': dict(),
            'config-locations': [
                    '~/.devenv.yaml',
                    '$devenv/etc/devenv/config.yaml',
                    '~/.config/devenv/config.yaml',
                    '/etc/devenv.yaml',
                    '/usr/etc/devenv.yaml',
                    ],
            'definitions': {
                'devenv': devenv_prefix,
                }
            }

    # Create top-level parser
    parser = argparse.ArgumentParser(
            description='Configure development environment based on predetermined configurations',
            formatter_class=argparse.RawTextHelpFormatter,
            add_help=False)
    parser.add_argument('--config-file', '-c', type=str,
            help=f'Path to configuration file. Defaults to {devenv_configuration["config-locations"][0]}',
            default=os.path.expanduser(devenv_configuration['config-locations'][0]))
    parser.add_argument('--help', '-h', help='View all program options',
            action=devenv.utils._HelpAction)

    # Create handle for registering other subparsers
    subparsers = parser.add_subparsers(help='sub-command --help', dest='command')
    help_parser = subparsers.add_parser("help", add_help=False)
    devenv.utils.add_default_parser_options(help_parser)

    # Add all subcommands
    devenv.subcommands.add_subparsers(subparsers)

    args = parser.parse_args()

    devenv.utils.setup_all_loggers(args)

    if args.verbose:
        args.verbose = True
        logger.setLevel(logging.INFO)

    if args.debug:
        args.debug = True
        logger.setLevel(logging.DEBUG)

    logger.debug(f'Starting with default configuration:\n%s' % pp.pformat(devenv_configuration))
    # Initialize configuration based on default config locations
    logger.debug('here')
    for path in devenv_configuration['config-locations']:
        logger.debug('Checking config location %s' % path)
        devenv.utils.load_config_file(devenv_configuration, path)

    # Apply command abbreviations
    if len(sys.argv) > 1:
        if sys.argv[1] in devenv_configuration['command-aliases'].keys():
            sys.argv[1] = devenv_configuration['command-aliases'][sys.argv[1]]

    # If user supplies another config file, load that too
    if args.config_file:
        devenv.utils.load_config_file(devenv_configuration, args.config_file)

    if args.command == 'help':
        print(devenv.utils.create_help(parser))
        sys.exit(0)

    logger.debug(f'Got args: {args}')

    devenv.subcommands.handle_subcommand(args, devenv_configuration)

    return 0
