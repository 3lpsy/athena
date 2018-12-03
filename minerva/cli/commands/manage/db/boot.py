from pathlib import Path
from minerva.logger import logger
from minerva.cli.commands.base import BaseCommand
from minerva.utils import minerva_path
from minerva.db.manager.session import load_database_engine

class ManageDbBootCommand(BaseCommand):

    def run(self):
        self.log_start()
        data_to_load_path = Path(minerva_path('load'))
        database_path = Path(minerva_path('manager.sqlite'))

        if not database_path.is_file():
            logger().info("Creating database file for manager at {}".format(str(database_path)))
            database_path.touch()

        logger().debug("Attaching session engine for manager database")
        load_database_engine()
