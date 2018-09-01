from athena.logger import logger

class BaseCommand(object):

    def __init__(self, options):
        self.options = options

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
    def make(cls, options):
        return cls(options)

    @classmethod
    def configure_parser(cls, parser):
        return parser
