import devenv.subcommands
import devenv.subcommands.dump
import devenv.subcommands.list
import devenv.subcommands.apply

def add_subparsers(subparsers) -> None:
    devenv.subcommands.dump.add_subparser(subparsers)
    devenv.subcommands.list.add_subparser(subparsers)
    devenv.subcommands.apply.add_subparser(subparsers)

def handle_subcommand(args, configs) -> None:

    if args.command == 'list':
        cmd = devenv.subcommands.list.List(args, configs)
    elif args.command == 'dump':
        cmd = devenv.subcommands.dump.Dump(args, configs)
    elif args.command == 'apply':
        cmd = devenv.subcommands.apply.Apply(args, configs)

    cmd.run()
