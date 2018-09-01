from pathlib import Path
from sys import exit
from athena.logger import logger
from athena.exceptions.base import BaseException
from athena.cli.commands.base import BaseCommand
from athena.utils import confirm, db_path

class ManageDbBootCommand(BaseCommand):

    def run(self):
        self.log_start()
        database_file_path = db_path('athena.sqlite')
        database_path = Path(database_file_path)

        if not database_path.is_file():
            logger().info("Creating database file for manager at {}".format(str(database_path)))
            database_path.touch()

        



    @classmethod
    def configure_parser(cls, parser):

        return parser
