from pathlib import Path
from sys import exit
from minerva.logger import logger
from minerva.cli.commands.base import BaseCommand
from minerva.utils import write_project_conf

class ProjectConfigGetCommand(BaseCommand):

    project_required = True

    def run(self):
        self.log_start()
        key = self.options.get('key')
        val = self.project_conf.get(key)
        print("{}:{}".format(key, val))

    @classmethod
    def configure_parser(cls, parser):
        parser.add_argument('--key', type=str, help="Config Key", choices=["db", "path", "name", "short_name"], required=True)
        return parser
