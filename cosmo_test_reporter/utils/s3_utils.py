import os
from boto.s3.connection import S3Connection
import logging
import params

__author__ = 'nirb'

logging.basicConfig()
logger = logging.getLogger('S3_UTILS')
logger.setLevel(logging.INFO)


def upload_file_to_s3_cosmo_quality(dir_path):
    """uploads the files in the local dir_path to s3 under <cosmo-quality>/dir_path"""
    conn = S3Connection(params.AWS_DEV_KEY_ID, params.AWS_DEV_SECRET_KEY)

    for root, _, files in os.walk(dir_path):
        for fname in files:
            bucket = conn.get_bucket("cosmo-quality")
            full_key_name = os.path.join(root, fname)
            key = bucket.new_key(full_key_name)
            key.set_contents_from_filename(full_key_name, policy='public-read')
            logger.info("uploaded file %s" % fname)
