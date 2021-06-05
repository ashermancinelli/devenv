import os
import logging
from typing import Dict
import devenv.configuration

logger = logging.getLogger('devenv.defaults')

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
        'e': 'edit',
        'st': 'status',
        }

# Default aliases for configurations
aliases = dict()
