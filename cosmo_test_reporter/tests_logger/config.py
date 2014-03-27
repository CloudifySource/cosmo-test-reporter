__author__ = 'nirb'


# flake8: NOQA
# logger configuration
from os import path


class LoggerConfiguration():

    def __init__(self, file_name):
        self.log_dir = path.expanduser('.')
        self.file = file_name
        self.logger_conf = {
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
                    "filename": "{0}/{1}.log".format(self.log_dir, self.file),
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
