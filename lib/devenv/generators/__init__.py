from typing import Dict
from abc import *
import devenv
import devenv.utils
import logging

logger = logging.getLogger('devenv.generators')

class CommandGenerator(ABC):
    @abstractmethod
    def generate(config: Dict[str, str]) -> str:
        ...


class BashGenerator(CommandGenerator):

    def __init__(self, args=None):
        self.args = args

    def add_devenv_variables(self, config) -> None:
        logger.debug('Adding devenv variables')
        for key, value in devenv.utils.get_devenv_variables(config, self.args).items():
            logger.debug(f'Exporting "{key}" as "{value}"')
            config['commands'].insert(0, f'export {key}={value}')

    def add_exported_variables(self, config) -> None:
        args = self.args
        if not args or not args.export:
            return
        
        logger.info('Adding exported variables')
        exported_vars = args.export.split(',')

        for var in exported_vars:
            logger.debug(f'Exporting variable "{var}"')
            
            # We're setting the variable via cli
            if '=' in var:
                key, value = var.split('=')
                logger.debug(f'Setting variable {key} to {value} in target environment via cli')

            # We're exporting the variable from host environment
            else:
                key = var
                value = os.environ[key]
                logger.debug(f'Setting variable {key} to {value} in target '
                        'environment via variable passthrough')

            config['commands'].insert(0, f'export {key}={value}')

    def add_commands(self, config) -> str:
        cmds = ''
        if 'commands' in config.keys():
            logger.info('Adding commands to command string')
            for c in config['commands']:
                logger.debug(f'Adding "{c}" to command string')
                cmds += '\n' + c

        cmds += '\n'
        return cmds

    def add_modules(self, config) -> str:
        cmds = ''
        if 'modules' in config.keys():
            logger.info('Adding "module load" commands to command string')
            for m in config['modules']:
                logger.debug(f'Adding "module load {m}" to command string')
                cmds += '\nmodule load ' + m
        return cmds

    def add_launch_command(self, config) -> str:
        cmds = ''
        if 'launch-command' in config.keys():
            logger.info(f'Adding launch command "{config["launch-command"]}" to command string')
            cmds += '\n' + config['launch-command'] + '\n'
        else:
            cmds += '\nbash\n'

        return cmds

    def generate(self, config: Dict[str, str]) -> str:
        '''Convert configuration into development environment init script'''

        logger.info('Building command from configuration')
        cmds = ''

        # If verbose, show all shell commands
        if self.args.verbose or self.args.debug:
            cmds += 'set -x\n'

        self.add_exported_variables(config)
        self.add_devenv_variables(config)

        cmds += self.add_modules(config)
        cmds += self.add_commands(config)

        if self.args.verbose or self.args.debug:
            cmds += 'set +x\n'

        cmds += self.add_launch_command(config)

        return cmds

def generate_script(args: str, config: Dict[str, str]) -> str:
    generator = BashGenerator(args=args)
    return generator.generate(config)
