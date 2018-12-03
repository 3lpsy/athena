from pathlib import Path
from sys import exit
import shutil
from minerva.cli.commands.base import BaseCommand
from minerva.exceptions import DataToLoadDirNotFound
from minerva.logger import logger
from minerva.utils import confirm, minerva_path

class ManageDbDeleteLoadDataCommand(BaseCommand):

    def run(self):
        self.log_start()
        data_to_load_path = Path(minerva_path('load'))

        if not data_to_load_path.is_dir():
            raise DataToLoadDirNotFound(data_to_load_path)

        message = "Do you really want to destroy the loadable data in {}".format(str(data_to_load_path))
        if not self.force():
            if confirm(message):
                message = "Are you sure you want to delete {}? This will delete any changes made to your loadable data".format(str(data_to_load_path))
                if confirm(message):
                    logger().warning("My the gods grant you mercy. Deleting {}".format(str(data_to_load_path)))
                    shutil.rmtree(str(data_to_load_path))
                    exit(0)
        else:
            message = "You opted to force delete load data. Interesting choice."
            logger().warning(message)
            shutil.rmtree(str(data_to_load_path))
            exit(0)

        logger().warning("I guess we won't do that then. Smart choice")
