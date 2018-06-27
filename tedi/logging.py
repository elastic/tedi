import logging
import logging.config
from os import environ


if 'TEDI_DEBUG' in environ and environ['TEDI_DEBUG'].lower() == 'true':
    log_level = 'DEBUG'
    log_format = 'verbose'
else:
    log_level = 'INFO'
    log_format = 'terse'

config = {
    'version': 1,
    'formatters': {
        'terse': {
            'format': '%(message)s'
        },
        'verbose': {
            'format': '%(name)s:%(lineno)s %(levelname)s: %(message)s'
        }
    },
    'handlers': {
        'console': {
            'class': 'logging.StreamHandler',
            'level': log_level,
            'formatter': log_format,
            'stream': 'ext://sys.stdout'
        }
    },
    'loggers': {
        'tedi': {
            'level': log_level,
            'handlers': ['console']
        }
    }
}


def getLogger(name=None):
    logging.config.dictConfig(config)
    logger = logging.getLogger(name)
    return logger
