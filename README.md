## Devenv - Manager for Complex Development Environments

To get started, just add ./bin to your PATH.

`devenv` has a few subcommands:

```console
$ ./bin/devenv -h
usage: devenv [-h] [--config-file CONFIG_FILE] [--full-help] [--verbose]
              [--vverbose] [--debug]
              {dump,list,apply} ...

Configure development environment based on predetermined configurations

positional arguments:
  {dump,list,apply}     sub-command help

optional arguments:
  -h, --help            show this help message and exit
  --config-file CONFIG_FILE, -c CONFIG_FILE
                        Path to configuration file. Defaults to ~/.devenv.yaml
  --full-help           Print extra long help information
  --verbose, -v         Verbose debugging information
  --vverbose, -vv       Extra verbose debugging information
  --debug, -L           Extra verbose debugging information
```

### Configuration Format

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

1. Exported variables from command line if --export flag is passed
2. Commands
3. Modules
4. Launch Command

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

would invoke the following command in a subshell:

```console
$ cd ~/workspace
$ module load gcc/7.4.0
$ srun -N 1 --pty bash
```

This development environment may be invoked either via `devenv -n myconfig`
or `devenv -n c`.

### Subcommands

#### Dump

`devenv dump` simply pretty-prints all information about valid development
environments currently configured.

#### List

`devenv list` lists the *names* of all the valid development environments currently configured.

#### Apply

`devenv apply <name>` applies the development environment given by name.

The `--export EXPORT` flag (eg `devenv apply <name> --export`) is meant to
replicate slurm's exporting functionality. For example:

```console
$ devenv apply myenv --export key1=value1,key2
```

would result in the following bash commands prefixing the rest of the commands:

```console
$ export key1=value1
$ export key2=<whatever the value of key2 was on the host system>
```

For example:

```console
$ export key2='value on host'
$ ./bin/devenv apply t --export key1=value1,key2
$ echo $key1
value1
$ echo $key2
value on host
```
