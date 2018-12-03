from os import getcwd
from os.path import abspath
from sys import exit
from minerva.logger import logger
from minerva.utils import read_projects_conf
from minerva.db.manager.session import load_database_engine

class BaseCommand(object):

    project_required = False
    loaded_required = False

    def __init__(self, options, app_conf, project, project_conf):
        self.options = options
        self.app_conf = app_conf
        self.project = project
        self.project_conf = project_conf

    def dispatch(self):
        self.prepare()
        self.run()
        self.postprocess()

    def prepare(self):
        self.loaded_is_required()
        self.load_project()

    def loaded_is_required(self):
        status = self.app_conf.get('loaded', 0)
        if not status and self.loaded_required:
            logger().critical("The manager database is not loaded. Please load it.")
            exit(1)

    def load_project(self):
        project_conf = None
        name_or_short_name = self.options.get('project', None)

        # load project_conf from cwd, fail if necessary
        if not name_or_short_name:
            for other_project_conf in read_projects_conf():
                if abspath(other_project_conf.get('path')) == abspath(str(getcwd())):
                    project_conf = other_project_conf
            if not project_conf and self.project_required:
                logger().critical("Project not found in current directory. Please specify a project name or change into the project directory")
                exit(1)

        # load project_conf from project_id, fail if necessary
        else:
            for other_project_conf in read_projects_conf():
                if abspath(other_project_conf.get('name')) == name_or_short_name or abspath(other_project_conf.get('short_name')) == name_or_short_name:
                    project_conf = other_project_conf
            if not project_conf and self.project_required:
                logger().critical("Project name or short name not found. Please specify a name or change into the project directory")
                exit(1)

        self.project_conf = project_conf

    def postprocess(self):
        pass

    def run(self):
        raise NotImplementedError()

    def force(self):
        if 'force' in self.options:
            return self.options['force']
        return False

    def log_start(self):
        logger().debug('Running Command: {}'.format(str(self.__class__.__name__)))
        logger().debug('Command Options: {}'.format(str(self.options)))

    @classmethod
    def make(cls, options, app_conf, project=None, project_conf=None):
        app_conf = app_conf or {}
        return cls(options, app_conf, project, project_conf)

    @classmethod
    def configure_parser(cls, parser):
        return parser
