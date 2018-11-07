import logging
import logging.config
from os import environ
from logging import Logger
from typing import List

emitted_warnings: List[str] = []

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
    logger.warn_once = warn_once
    return logger


# FIXME: Make a custom logger by inheriting from Logger
def warn_once(logger: Logger, message: str):
    if message not in emitted_warnings:
        logger.warning(message)
        emitted_warnings.append(message)
