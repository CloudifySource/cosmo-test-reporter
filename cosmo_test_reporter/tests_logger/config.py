__author__ = 'nirb'


# flake8: NOQA
# logger configuration
from os import path
LOG_DIR = path.expanduser('./')
MODULE = 'test'
LOGGER = {
    "version": 1,
    "formatters": {
        "file": {
            "format": "%(asctime)s [%(levelname)s] %(message)s"
        },
        "console": {
            "format": "%(message)s"
        }
    },
    "handlers": {
        "file": {
            "class": "logging.handlers.RotatingFileHandler",
            "formatter": "file",
            "level": "DEBUG",
            "filename": "{0}/{1}.log".format(LOG_DIR, MODULE),
            "maxBytes": "5000000",
            "backupCount": "20"
        },
        "console": {
            "class": "logging.StreamHandler",
            "stream": "ext://sys.stdout",
            "formatter": "console"
        }
    },
    "loggers": {
        "main": {
            "handlers": [
                "console",
                'file'
            ]
        },
        "file": {
            "handlers": [
                'file'
            ]
        }
    }
}
