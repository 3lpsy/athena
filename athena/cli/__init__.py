from athena.cli.commands import ProjectInitializeCommand

from .parser import parser, subparser
from .cli import Cli

cli = Cli(parser, subparser)

cli.register('init', ProjectInitializeCommand)
