import argparse
from athena.cli.commands import HelpCommand

# create the top-level parser
parser = argparse.ArgumentParser(add_help=False)
parser.add_argument('-v', '--verbose', '-v', action='count', default=0)
parser.add_argument('--force', action='store_true', default=False)
parser.add_argument('-h', '--help', action=HelpCommand, help='show this help message and exit')
parser.add_argument('--directory', type=str, help="Directory to initialize")
# add custom help

# create sub parser container
subparser = parser.add_subparsers(title="commands", dest="command")
