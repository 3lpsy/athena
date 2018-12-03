from pathlib import Path
from sys import exit
from minerva.logger import logger
from minerva.cli.commands.base import BaseCommand
from minerva.utils import read_projects_conf

class ProjectListCommand(BaseCommand):
    project_required = True
    make_sure_user_is_logged_in = True
    def run(self):
        self.log_start()
        projects = read_projects_conf()
        for project in projects:
            print("{} ({})".format(project.get('name'), project.get('short_name')))
