def make_handler(level='INFO', formatter='short', handler='logging.StreamHandler', **kwargs):
    config = {
        'level': level,
        'formatter': formatter,
        'class': handler,
    }

    if kwargs and len(kwargs) > 0:
        for k, v in kwargs.items():
            config[k] = v
    return config

def make_formatter(format='%(asctime)s %(levelname)s %(name)s: %(message)s'):
    return {
        'format': format,
    }

def make_logger(handlers=None, level='INFO', **kwargs):
    handlers = handlers or ['console']
    config = {
        'handlers': handlers,
        'level': level,
    }
    if kwargs and len(kwargs) > 0:
        for k, v in kwargs.items():
            config[k] = v
    return config

def make_config():
    config = {
        'disable_existing_loggers': False,
        'version': 1
    }
    config['formatters'] = {
        'tiny': make_formatter('%(levelname)s: %(message)s'),
        'short': make_formatter()
    }
    config['handlers'] = {
        'console': make_handler(formatter='tiny')
    }
    config['loggers'] = {
        '': make_logger(handlers=['console'], level='INFO'),
        'plugins': make_logger(handlers=['console'], level='INFO', propagate=True)
    }
    return config
