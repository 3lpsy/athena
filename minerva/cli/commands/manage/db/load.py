from pathlib import Path
from os.path import join
from sys import exit
import json
from minerva.logger import logger
from minerva.exceptions import DataToLoadDirNotFound
from minerva.cli.commands.base import BaseCommand
from minerva.utils import only, minerva_path, write_minerva_conf
from minerva.db.manager.session import load_database_tables
from minerva.db.manager.models import Service, Task
from minerva.db.manager.session import managersession

class ManageDbLoadCommand(BaseCommand):

    def run(self):
        self.log_start()
        data_to_load_path = Path(minerva_path('load'))
        database_path = Path(minerva_path('manager.sqlite'))

        if not database_path.is_file():
            if not data_to_load_path.is_dir():
                raise DataToLoadDirNotFound(data_to_load_path)
            logger().info("Creating database file for manager at {}".format(str(database_path)))
            database_path.touch()

        load_database_tables()

        if not self.app_conf.get('loaded', 0):
            self.load_manager_data_full(data_to_load_path)
        else:
            self.load_manager_data_update(data_to_load_path)

    def load_manager_data_full(self, data_to_load_path):
        logger().info("Performing full load of data")

        services_path = Path(join(str(data_to_load_path), "services.json"))
        with open(services_path, "r", encoding="utf-8") as infile:
            unloaded_services = json.loads(infile.read())

        tasks_path = Path(join(str(data_to_load_path), "tasks.json"))
        with open(tasks_path, "r", encoding="utf-8") as infile:
            unloaded_tasks= json.loads(infile.read())

        s = managersession()

        logger().info("Loading services.json into database")
        for unloaded_service in unloaded_services:
            data = only(unloaded_service, ["name", "code", "description"])
            new_service = Service(**data)
            s.add(new_service)
            logger().debug("Loaded Service: {}".format(new_service.name))

        logger().info("Loading tasks.json into database")
        for unloaded_task in unloaded_tasks:
            data = only(unloaded_task, ["name", "code", "description", "skippable"])
            new_task = Task(**data)
            s.add(new_task)
            logger().debug("Loaded Task: {}".format(new_task.name))

        s.commit()

        self.app_conf.update({'loaded':1})
        write_minerva_conf(self.app_conf)

    def load_manager_data_update(self, data_to_load_path):
        logger().info("Performing update load of data")

        services_path = Path(join(str(data_to_load_path), "services.json"))

        with open(services_path, "r", encoding="utf-8") as infile:
            unloaded_services = json.loads(infile.read())

        tasks_path = Path(join(str(data_to_load_path), "tasks.json"))
        with open(tasks_path, "r", encoding="utf-8") as infile:
            unloaded_tasks= json.loads(infile.read())

        s = managersession()

        logger().info("Loading updated services.json into database")
        for unloaded_service in unloaded_services:
            cols = ["name", "code", "description"]
            data = only(unloaded_service, cols, strict=True)
            code = data['code']
            current_service = s.query(Service).filter_by(code=code).first()
            if current_service:
                for col in cols:
                    setattr(current_service, col, data[col])
            else:
                new_service = Service(**data)
                s.add(new_service)

        logger().info("Loading updated tasks.json into database")
        for unloaded_task in unloaded_tasks:
            cols = ["name", "code", "description", "skippable"]
            data = only(unloaded_task, cols, strict=True)
            code = data['code']
            current_task = s.query(Task).filter_by(code=code).first()
            if current_task:
                for col in cols:
                    setattr(current_task, col, data[col])
            else:
                new_task = Task(**data)
                s.add(new_task)

        s.commit()

    @classmethod
    def configure_parser(cls, parser):
        return parser
