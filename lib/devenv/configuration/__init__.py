import os
import logging
import yaml
import argparse
import sys
import devenv
from typing import List
import pprint
pp = pprint.PrettyPrinter(indent=4)

logger = logging.getLogger('devenv.configuration')

def set_logging_attrs(args, logger) -> None:
    if args.verbose:
        logger.setLevel(logging.INFO)

    if args.vverbose or args.debug:
        logger.setLevel(logging.DEBUG)
        logger.debug('Debug output enabled')


def apply_shorthand_commands(argv: List[str]) -> None:
    if len(argv) < 2:
        return

    logging.debug(f'Applying shorthands to args "{argv}"')
    if argv[1] in devenv.defaults.command_shorthands.keys():
        argv[1] = devenv.defaults.command_shorthands[argv[1]]


def check_config_file(args) -> None:
    set_logging_attrs(args, logger)
    # If the config file doesn't exist, check the default locations until we find one that does
    config_file = os.path.abspath(args.config_file)
    default_loc_i = 0
    while not os.path.exists(config_file):
        logging.debug(f"{__file__} Couldn't find file {config_file}")
        config_file = os.path.expanduser(defaults.config_locations[default_loc_i])
        logging.debug(f'Checking {config_file}')
        default_loc_i += 1
    args.config_file = config_file

    logging.debug(f'Using config file {args.config_file}')
    # If we still don't have a valid config file after checking default locations,
    # let's just give up.
    if not os.path.exists(args.config_file):
        raise ValueError(f'Configuration file {args.config_file.strip()} does not exist!'
                ' Please pass `--config` flag or create config file ~/.devenv.yaml.')

def merge_config_file(configs, aliases, args) -> None:
    # Add the configs from the config file to our internal dict of configs
    with open(args.config_file, 'r') as f:
        new_values = yaml.full_load(f)
        logging.debug(f'Got the following values from config file:\n{pp.pformat(new_values)}')

        if 'configs' in new_values.keys():
            logging.info('Updating configurations from config file')
            configs.update(new_values['configs'])

        if 'aliases' in new_values.keys():
            logging.info('Updating aliases from config file')
            aliases.update(new_values['aliases'])

    logging.debug('Checking for conflicts between aliases and configs')
    if len(set(configs.keys()).intersection(aliases.keys())) > 0:
        raise ValueError('Got conflict between configuration names and aliases!')

def add_default_parser_options(parser):
    parser.add_argument('--verbose', '-v', help='Verbose debugging information', action='store_true')
    parser.add_argument('--debug', '-L', help='Extra verbose debugging information', action='store_true')
    return parser
