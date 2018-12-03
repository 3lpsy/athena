from minerva.cli.commands import ManageDbTeardownCommand, ManageDbLoadCommand, ManageDbDeleteLoadDataCommand, ManageServiceListCommand

from minerva.cli.commands import ProjectCreateCommand, ProjectDestroyCommand, ProjectListCommand, ProjectConfigSetCommand, ProjectConfigGetCommand, ProjectConfigListCommand

from .parser import parser, subparser
from .cli import Cli

def _attach_project_commands(cli):
    cli.register('create', ProjectCreateCommand)
    cli.register('destroy', ProjectDestroyCommand)

    cli.register('list', ProjectListCommand)
    cli.register('list-config', ProjectConfigListCommand)
    cli.register('get-config', ProjectConfigGetCommand)
    cli.register('set-config', ProjectConfigSetCommand)

def _attach_manager_commands(cli):
    cli.register('list-services', ManageServiceListCommand)
    cli.register('delete-load-data', ManageDbDeleteLoadDataCommand)
    cli.register('load', ManageDbLoadCommand)
    cli.register('teardown', ManageDbTeardownCommand)

def make_cli(type=None):
    cli = Cli(parser, subparser)

    if not type:
        _attach_project_commands(cli)
        _attach_manager_commands(cli)
    elif type == 'manager':
        _attach_manager_commands(cli)
    elif type == 'project':
        _attach_project_commands(cli)

    return cli
