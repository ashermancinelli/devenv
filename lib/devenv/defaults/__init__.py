import textwrap

extra_help = textwrap.dedent('''
Full Help Message:
-------------------------------------------------------------------------------

The configuration files must have the following form:

```yaml
# ~/.devenv.yaml
configs:
    config-name:
        commands: []
        modules: []
        launch-command: ''

aliases:
    alias1: value1
```

The commands are built in the following order:

    0. Exported variables from command line if --export flag is passed
    1. Commands
    2. Modules
    3. `srun` command

For example, the following config:
```yaml
# ~/.devenv.yaml
configs:
    myconfig:
        commands:
          - cd ~/workspace
        modules:
          - gcc/7.4.0
        launch-command: 'srun -N 1 --pty bash'

aliases:
    c: myconfig
```

would invoke the following command:

    $ cd ~/workspace
    $ module load gcc/7.4.0
    $ srun -N 1 --pty bash

This development environment may be invoked either via `devenv -n myconfig`
or `devenv -n c`.

-------------------------------------------------------------------------------
''')

# Default locations for config files
config_locations = [
        '~/.devenv.yaml',
        '~/.config/devenv/config.yaml',
        '/etc/devenv.yaml',
        '/usr/etc/devenv.yaml',
        ]

configs = {
        'default': {
              'launch-command': '',
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
