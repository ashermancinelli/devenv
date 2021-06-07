import argparse
import yaml
from typing import List, Dict, Optional
import os
import logging
import devenv

if int(yaml.__version__.split('.')[0]) < 5:
    yaml_load_fn = yaml.load
else:
    yaml_load_fn = yaml.full_load

logger = logging.getLogger('devenv.utils')

class DotDict(dict):
    """dot.notation access to dictionary attributes"""
    __getattr__ = dict.get
    __setattr__ = dict.__setitem__
    __delattr__ = dict.__delitem__

def make_version_info(git_description: str) -> Dict[str, str]:
    if '-' in git_description:
        return devenv.utils.DotDict({
            'label': git_description,
            'tag': git_description.split('-')[0],
            'revision': git_description.split('-')[1],
            'commit': git_description.split('-')[2][1:],
            })

    # If '-' is not in the git description, we're working directly on a tagged branch
    return devenv.utils.DotDict({
        'label': git_description,
        'tag': git_description,
        'revision': 0,
        'commit': None
        })

def get_devenv_variables(config, args) -> Dict[str, str]:
    env = dict()
    env['DEVENV_LAYERS'] = int(os.environ.get('DEVENV_LAYERS', 0)) + 1
    env['DEVENV_ENV_NAME'] = args.name
    return env

def set_logging_attrs(args, logger) -> None:
    if args.verbose:
        logger.setLevel(logging.INFO)

    if args.debug:
        logger.setLevel(logging.DEBUG)
        logger.debug('Debug output enabled')

def setup_all_loggers(args: argparse.Namespace):
    set_logging_attrs(args, devenv.utils.logger)
    set_logging_attrs(args, devenv.subcommands.apply.logger)
    set_logging_attrs(args, devenv.subcommands.describe.logger)
    set_logging_attrs(args, devenv.subcommands.edit.logger)
    set_logging_attrs(args, devenv.subcommands.list.logger)
    set_logging_attrs(args, devenv.subcommands.status.logger)
    set_logging_attrs(args, devenv.subcommands.version.logger)
    set_logging_attrs(args, devenv.subcommands.update.logger)
    set_logging_attrs(args, devenv.generators.logger)

def interpolate(string, devinitions: Dict[str, str]):
    '''If "$key" exists in string, replace "$key" with values[key]'''

    interpolated = string

    for k in devinitions.keys():
        logger.debug('Checking if key "%s" should be interpolated in string "%s"' % (k, string))
        if f'${k}' in string:
            interpolated = string.replace(f'${k}', devinitions[k])

    return interpolated

def load_config_file(configuration: Dict[str, str], path: str):


    interpolate(path, configuration['definitions'])
    if os.path.exists(path):
        logger.debug('Loading path %s' % path)
        contents = ''
        with open(path, 'r') as f:
            for line in f:
                line = line.replace('\n', '')
                interpolate(line, configuration['definitions'])
                contents += line + '\n'
        config = yaml_load_fn(contents)
        configuration.update(config['devenv'])


def create_help(parser) -> str:
    help = parser.format_help()
    # retrieve subparsers from parser
    subparsers_actions = [
        action for action in parser._actions
        if isinstance(action, argparse._SubParsersAction)]

    # there will probably only be one subparser_action,
    # but better save than sorry
    for subparsers_action in subparsers_actions:
        # get all subparsers and print help
        for choice, subparser in subparsers_action.choices.items():
            help += '\n' + '-' * 80 + '\n'
            help += f'\nHelp for subcommand "{choice}"\n'
            help += '-' * 30 + '\n'
            help += subparser.format_help()
        help += '\n' + '-' * 80

    return help

# See https://stackoverflow.com/questions/20094215/argparse-subparser-monolithic-help-output
class _HelpAction(argparse._HelpAction):

    def __call__(self, parser, namespace, values, option_string=None):
        print(create_help(parser))
        parser.exit()


def check_config_file(args) -> None:
    set_logging_attrs(args, logger)
    # If the config file doesn't exist, check the default locations until we find one that does
    config_file = os.path.abspath(args.config_file)
    default_loc_i = 0
    while not os.path.exists(config_file):
        logging.debug(f"{__file__} Couldn't find file {config_file}")
        config_file = os.path.expanduser(config_locations[default_loc_i])
        logging.debug(f'Checking {config_file}')
        default_loc_i += 1
    args.config_file = config_file

    logging.debug(f'Using config file {args.config_file}')
    # If we still don't have a valid config file after checking default locations,
    # let's just give up.
    if not os.path.exists(args.config_file):
        raise ValueError(f'Configuration file {args.config_file.strip()} does not exist!'
                ' Please pass `--config` flag or create config file ~/.devenv.yaml.')

def merge_config_file(config: Dict[str, str], args: argparse.Namespace) -> None:

    # Add the configs from the config file to our internal dict of configs
    with open(args.config_file, 'r') as f:
        new_values = yaml_load_fn(f)['devenv']
        logging.debug(f'Got the following values from config file:\n{pp.pformat(new_values)}')

        if 'environments' in new_values.keys():
            logging.info('Updating configurations from config file')
            config['environments'].update(new_values['configs'])

        if 'aliases' in new_values.keys():
            logging.info('Updating aliases from config file')
            config['aliases'].update(new_values['aliases'])

    logging.debug('Checking for conflicts between aliases and configs')
    if len(set(config['environments'].keys()).intersection(config['aliases'].keys())) > 0:
        raise ValueError('Got conflict between configuration names and aliases!')

def add_default_parser_options(parser):
    parser.add_argument('--verbose', '-v', help='Verbose debugging information', action='store_true')
    parser.add_argument('--debug', '-L', help='Extra verbose debugging information', action='store_true')
