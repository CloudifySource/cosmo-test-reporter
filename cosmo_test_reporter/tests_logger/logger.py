import logging
import logging.config
import os
import sys
import config

__author__ = 'nirb'


def init_logger(file_name):
    if os.path.isfile(config.LOG_DIR):
        sys.exit('file {0} exists - cloudify log directory cannot be created '
                 'there. please remove the file and try again.'.format(config.LOG_DIR))

    try:
        config.MODULE = file_name
        logfile = config.LOGGER['handlers']['file']['filename']
        d = os.path.dirname(logfile)
        if not os.path.exists(d):
            os.makedirs(d)
        logging.config.dictConfig(config.LOGGER)
        lgr = logging.getLogger('main')
        lgr.setLevel(logging.INFO)
        flgr = logging.getLogger('file')
        flgr.setLevel(logging.DEBUG)
    except ValueError:
        sys.exit('could not initialize logger.'
                 ' verify your logger config'
                 ' and permissions to write to {0}'.format(logfile))
    return lgr
