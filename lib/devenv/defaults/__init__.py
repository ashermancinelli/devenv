import os
import logging
from typing import Dict
import devenv.configuration

logger = logging.getLogger('devenv.defaults')

def get_devenv_variables(config, args) -> Dict[str, str]:
    devenv.configuration.set_logging_attrs(args, logger)
    env = dict()
    env['DEVENV_LAYERS'] = int(os.environ.get('DEVENV_LAYERS', 0)) + 1
    env['DEVENV_ENV_NAME'] = args.name
    return env

# Default locations for config files
config_locations = [
        '~/.devenv.yaml',
        '~/.config/devenv/config.yaml',
        '/etc/devenv.yaml',
        '/usr/etc/devenv.yaml',
        ]

configs = {
        'default': {
              'launch-command': None,
              'modules': [],
              'commands': [],
            },
        }

command_shorthands = {
        'ap': 'apply',
        'du': 'dump',
        'ls': 'list',
        'ed': 'edit',
        }

# Default aliases for configurations
aliases = dict()
