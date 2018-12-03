from .base import BaseException
from minerva.logger import logger

class DataToLoadDirNotFound(BaseException):
    def __init__(self, directory):
        message = "Cannot find {}. This file is required to load data into the manager database with information such as tasks, commands, and other values.".format(directory)
        super().__init__(message)
