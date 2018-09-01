from pathlib import Path
from os.path import join
from sys import exit
from athena.logger import logger
from athena.exceptions.base import BaseException
from athena.cli.commands.base import BaseCommand
from athena.utils import confirm

class ProjectInitializeCommand(BaseCommand):

    def run(self):
        self.log_start()
        project_path = self.options['directory']
        project_path = Path(project_path).resolve()
        logger().info('Initializing: {}'.format(str(project_path)))
        self.make_project_directory(project_path)
        self.make_sub_directories(project_path)

    def make_project_directory(self, project_path):
        self.make_directory(project_path)

    def make_sub_directories(self, project_path):
        directory_names = ['data', 'reports', '.db', 'scripts']
        directory_paths = [Path(join(project_path, d)) for d in directory_names]
        for directory_path in directory_paths:
            self.make_directory(directory_path)
        logger().warning('Directories created ({}). Do not delete the ".db" folder please! '.format(directory_names))


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

    @classmethod
    def configure_parser(cls, parser):
        parser.add_argument('directory', type=str, help="Directory to initialize")
        return parser
