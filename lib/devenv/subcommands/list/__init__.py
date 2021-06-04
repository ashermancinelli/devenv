from devenv.subcommands.base_command import Command
import devenv.configuration

list_parser = None

def add_subparser(subparsers):
    list_parser = subparsers.add_parser("list")
    devenv.configuration.add_default_parser_options(list_parser)

class List(Command):
    def __init__(self, args, configs):
        super().__init__(args, configs)

    def run(self):
        for cfg in self.configs.keys():
            print(cfg)
