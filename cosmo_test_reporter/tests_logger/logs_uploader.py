from cosmo_test_reporter.utils import s3_utils
from cosmo_test_reporter.utils import params

__author__ = 'nirb'


def upload_logs():
    s3_utils.upload_file_to_s3_cosmo_quality('../{0}'.format(params.BUILD_NUMBER))

upload_logs()