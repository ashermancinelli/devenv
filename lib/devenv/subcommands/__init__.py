import logging
import devenv
import devenv.subcommands.dump
import devenv.subcommands.status
import devenv.subcommands.version
import devenv.subcommands.edit
import devenv.subcommands.list
import devenv.subcommands.apply

logger = logging.getLogger('devenv.subcommands')

def add_subparsers(subparsers) -> None:
    devenv.subcommands.edit.add_subparser(subparsers)
    devenv.subcommands.dump.add_subparser(subparsers)
    devenv.subcommands.list.add_subparser(subparsers)
    devenv.subcommands.apply.add_subparser(subparsers)
    devenv.subcommands.version.add_subparser(subparsers)
    devenv.subcommands.status.add_subparser(subparsers)

def handle_subcommand(args, configs) -> None:

    command_mapping = {
            'list': devenv.subcommands.list.List,
            'apply': devenv.subcommands.apply.Apply,
            'dump': devenv.subcommands.dump.Dump,
            'edit': devenv.subcommands.edit.Edit,
            'version': devenv.subcommands.version.Version,
            'status': devenv.subcommands.status.Status,
            }

    devenv.configuration.set_logging_attrs(args, logger)

    logger.debug(f'Got command "{args.command}"')
    cmd = command_mapping[args.command](args, configs)

    logger.debug('Running command')
    cmd.run()
