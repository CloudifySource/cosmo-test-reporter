import logging
import logging.config
import os
import sys
import config

__author__ = 'nirb'


def init_logger(file_name):

    log_config = config.LoggerConfiguration(file_name)

    if os.path.isfile(log_config.log_dir):
        sys.exit('file {0} exists - cloudify log directory cannot be created '
                 'there. please remove the file and try again.'.format(log_config.log_dir))

    try:
        logfile = log_config.logger_conf['handlers']['file']['filename']
        d = os.path.dirname(logfile)
        if not os.path.exists(d):
            os.makedirs(d)
        logging.config.dictConfig(log_config.logger_conf)
        lgr = logging.getLogger('main')
        lgr.setLevel(logging.INFO)
        flgr = logging.getLogger('file')
        flgr.setLevel(logging.DEBUG)
    except ValueError:
        sys.exit('could not initialize logger.'
                 ' verify your logger config'
                 ' and permissions to write to {0}'.format(logfile))
    return lgr
