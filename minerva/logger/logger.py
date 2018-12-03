import logging
import logging.config
from minerva.logger.config import make_config, make_handler, make_logger
from logging_tree import printout

SHORT_FORMAT = logging.Formatter('%(asctime)s %(levelname)s %(name)s: %(message)s')
TINY_FORMAT = logging.Formatter('%(levelname)s: %(message)s')

def logger():
    if not logging.getLogger('cli'):
        raise Exception("Logger not configured yet. Sorry")
    return logging.getLogger('cli')

def setup_logger(app_conf=None):
    app_conf = app_conf or {'log_level': 'INFO'}
    level = getattr(logging, app_conf.get('log_level').upper(), logging.INFO)

    cli_logger = logging.getLogger('cli')
    cli_logger.setLevel(level)

    # console handler
    chandler = logging.StreamHandler()

    chandler.setFormatter(TINY_FORMAT)
    cli_logger.addHandler(chandler)

    # file handler
    fhandler = logging.handlers.RotatingFileHandler(
        app_conf.get('log_path', 'minerva.log'),
        maxBytes=10485760,
        backupCount=5,
        mode='a',
    )

    fhandler.setFormatter(SHORT_FORMAT)
    cli_logger.addHandler(fhandler)
