from pathlib import Path
from os import getcwd
from os.path import join, basename
from sys import exit
import re
import argparse
from sys import exit
from minerva.logger import logger
from minerva.exceptions.base import BaseException
from minerva.cli.commands.base import BaseCommand
from minerva.db.project.session import load_database_engine, load_database_tables
from minerva.utils import confirm, write_project_conf
from minerva.db.manager.session import managersession
from minerva.db.manager.models import Service

def alphadash(val, pat=re.compile(r"[a-z0-9A-Z_-]{2,32}")):
    if not pat.match(val):
        print("The short name must be alphanumeric and contain no spaces")
        raise argparse.ArgumentTypeError
    return val

class ProjectCreateCommand(BaseCommand):
    require_loaded = True

    def run(self):
        self.validate_service_code(self.options.get('type'))
        self.log_start()
        project_path = Path(self.resolve_path()).resolve()
        project_name = self.resolve_name(project_path)
        logger().info('Initializing: {}'.format(str(project_path)))
        self.make_project_directory(project_path)
        self.make_sub_directories(project_path)
        project_short_name = self.resolve_short_name(project_name)
        db_path = join(join(project_path, '.db'), project_short_name + ".sqlite")
        self.make_db(db_path)
        self.register_project(project_name, project_short_name, project_path, db_path)

    def resolve_short_name(self, project_name):
        project_short_name= self.options['short_name']
        if not project_short_name:
            project_short_name = re.sub('[^\w\-_\.]', '_', project_name)
        return project_short_name

    def resolve_path(self):
        project_path = self.options['directory']
        if not project_path:
            project_path = getcwd()
        return project_path

    def resolve_name(self, project_path=None):
        project_name = self.options['name']
        if not project_name:
            project_name = basename(str(project_path))
        return project_name

    def make_db(self, db_path):
        load_database_engine(db_path)
        logger().info('Creating project database at {}'.format(db_path))
        load_database_tables(db_path)
        populate_project_from_service_code(self.options.get('type').upper()))


    def register_project(self, project_name, project_short_name, project_path, db_path):
        project_data = {}
        project_data['name'] = project_name
        project_data['short_name'] = project_short_name
        project_data['path'] = str(project_path)
        project_data['db'] = str(db_path)

        logger().info('Adding project to projects.json'.format(db_path))

        write_project_conf(project_data)

    def make_project_directory(self, project_path):
        self.make_directory(project_path)

    def make_directory(self, path):
        if path.is_file():
            message = "Cannot initialize directory. A file exists at that location"
            logger().critical(message)
            raise BaseException(message)
        elif path.is_dir():
            if self.force():
                message = "Directory exists! Continuing anyways! ({})".format(str(path))
                logger().warning(message)
            else:
                message = "Target Directory Exists. Continue?"
                if not confirm(message):
                    logger().info('You opted not to continue creating the directory. I respect your decision')
                    exit(0)
        else:
            path.mkdir()

    def make_sub_directories(self, project_path):
        directory_names = ['data', 'reports', '.db', 'scripts']
        directory_paths = [Path(join(project_path, d)) for d in directory_names]
        for directory_path in directory_paths:
            logger().info('Creating {}'.format(str(directory_path)))
            self.make_directory(directory_path)
        logger().warning('Directories created. Do not delete the ".db" folder please! '.format(directory_names))

    def validate_service_code(self, code):
        service_codes = managersession().query(Service).all()
        if code.upper() not in [s.code.upper() for s in service_codes]:
            print("The type must be valid service code({})".format([s.code.upper() for s in service_codes]))
            exit(1)
        return code.upper()

    @classmethod
    def configure_parser(cls, parser):
        parser.add_argument('--name', type=str, help="Project Name")
        parser.add_argument('--short-name', help="Project Short Name", type=alphadash)
        parser.add_argument('--directory', type=str, help="Directory to initialize")
        parser.add_argument('--type', type=str, help="Type of service", required=True)

        return parser
