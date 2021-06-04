from typing import Dict
from abc import *
import logging

logger = logging.getLogger('devenv.generators')

class CommandGenerator(ABC):
    @abstractmethod
    def generate(config: Dict[str, str]) -> str:
        ...


class BashGenerator(CommandGenerator):

    def __init__(self, args=None):
        self.args = args

    def add_exported_variables(self, config) -> None:
        args = self.args
        if not args or not args.export:
            return
        
        logging.info('Adding exported variables')
        exported_vars = args.export.split(',')

        for var in exported_vars:
            logging.debug(f'Exporting variable "{var}"')
            
            # We're setting the variable via cli
            if '=' in var:
                key, value = var.split('=')
                logging.debug(f'Setting variable {key} to {value} in target environment via cli')

            # We're exporting the variable from host environment
            else:
                key = var
                value = os.environ[key]
                logging.debug(f'Setting variable {key} to {value} in target '
                        'environment via variable passthrough')

            config['commands'].insert(0, f'export {key}={value}')

    def add_commands(self, config) -> str:
        cmds = ''
        if 'commands' in config.keys():
            logging.info('Adding commands to command string')
            for c in config['commands']:
                logging.debug(f'Adding "{c}" to command string')
                cmds += '\n' + c
        return cmds

    def add_modules(self, config) -> str:
        cmds = ''
        if 'modules' in config.keys():
            logging.info('Adding "module load" commands to command string')
            for m in config['modules']:
                logging.debug(f'Adding "module load {m}" to command string')
                cmds += '\nmodule load ' + m
        return cmds

    def add_launch_command(self, config) -> str:
        cmds = ''
        if 'launch-command' in config.keys():
            logging.info(f'Adding launch command "{config["launch-command"]}" to command string')
            cmds += '\n' + config['launch-command']
        else:
            cmds += '\nbash'

        return cmds

    def generate(self, config: Dict[str, str]) -> str:
        '''Convert configuration into development environment init script'''

        logging.info('Building command from configuration')
        cmds = ''

        self.add_exported_variables(config)

        cmds += self.add_commands(config)
        cmds += self.add_modules(config)
        cmds += self.add_launch_command(config)

        return cmds

def generate_script(args: str, config: Dict[str, str]) -> str:
    devenv.configuration.set_logging_attrs(args, logger)
    generator = BashGenerator(args=args)
    return generator.generate(config)
