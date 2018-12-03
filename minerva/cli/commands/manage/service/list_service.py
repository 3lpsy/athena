from pathlib import Path
from sys import exit
from minerva.logger import logger
from minerva.cli.commands.base import BaseCommand
from minerva.db.manager.session import managersession
from minerva.db.manager.models import Service

class ManageServiceListCommand(BaseCommand):
    loaded_required = True

    def run(self):
        self.log_start()
        services = managersession().query(Service).all()
        for service in services:
            print("{} ({})".format(service.name, service.code))
