from pathlib import Path
from sys import exit
from minerva.logger import logger
from minerva.cli.commands.base import BaseCommand
from minerva.utils import minerva_path
from minerva.utils import confirm

class ManageDbTeardownCommand(BaseCommand):

    def run(self):
        self.log_start()
        database_path = Path(minerva_path('manager.sqlite'))

        if not database_path.is_file():
            logger().warning("Manager database path does not exist. Skipping".format(str(database_path)))
            return

        message = "Do you really want to destroy the manager database"
        if not self.force():
            if confirm(message):
                logger().warning("Deleting manager database")
                database_path.unlink()
                exit(0)
            else:
                logger().warning("I guess we won't do that then")
        else:
            logger().warning("Deleting manager database by force")
            database_path.unlink()
