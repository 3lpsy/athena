from pathlib import Path
from sys import exit
from minerva.logger import logger
from minerva.cli.commands.base import BaseCommand
from minerva.utils import remove_project_conf, confirm

class ProjectDestroyCommand(BaseCommand):

    project_required = True

    def run(self):
        self.log_start()
        message = "Are you sure you want to delete project {} located at {}".format(self.project_conf.get('name'), self.project_conf.get('path'))
        if not self.force() and confirm(message):
            logger().warning("Removing project {} located at {}".format(self.project_conf.get('name'), self.project_conf.get('path')))
            remove_project_conf(self.project_conf)
