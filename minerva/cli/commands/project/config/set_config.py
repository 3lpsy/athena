from pathlib import Path
from sys import exit
from minerva.logger import logger
from minerva.cli.commands.base import BaseCommand
from minerva.utils import write_project_conf

class ProjectConfigSetCommand(BaseCommand):

    project_required = True

    def run(self):
        self.log_start()
        key = self.options.get('key')
        oldval = self.project_conf.get(key)
        val = self.options.get('value')
        self.project_conf.update({key: val})
        write_project_conf(self.project_conf)
        print("Old Value: {}:{}".format(key, oldval))
        print("New Value: {}:{}".format(key, val))

    @classmethod
    def configure_parser(cls, parser):
        parser.add_argument('--key', type=str, help="Config Key", choices=["db", "path", "name", "short_name"], required=True)
        parser.add_argument('--value', type=str, help="Value to set", required=True)
        return parser
