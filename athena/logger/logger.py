import logging
import logging.config

from athena.logger.config import make_config, make_handler, make_logger

config = make_config()

logging.config.dictConfig(config)

_logger = None

def logger():
    global _logger
    if _logger is None:
        return logging.getLogger()
    return _logger

def setup_cli(filename):
    config = make_config()
    fhandler = make_handler(
        level='INFO',
        formatter='short',
        handler='logging.handlers.RotatingFileHandler',
        filename=filename,
        mode='a',
        maxBytes=10485760,
        backupCount=5
    )
    config['handlers']['file'] = fhandler
    config['loggers']['cli'] = make_logger(handlers=['console', 'file'], level='INFO')
    config['loggers']['cli']['handlers'] = ['console', 'file']
    logging.config.dictConfig(config)
    _logger = logging.getLogger('cli')
