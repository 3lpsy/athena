from pathlib import Path
from sys import exit
from minerva.logger import logger
from minerva.cli.commands.base import BaseCommand
from minerva.utils import write_project_conf

class ProjectConfigListCommand(BaseCommand):

    project_required = True

    def run(self):
        self.log_start()
        for key, val in self.project_conf.items():
            print("{}:{}".format(key, val))
