from __future__ import absolute_import, unicode_literals

from regonwye.aws.conf import *
from decouple import config

from boto.s3.connection import S3Connection

s3 = S3Connection(os.environ['AWS_ACCESS_KEY_ID'], os.environ['AWS_SECRET_ACCESS_KEY'])

from .base import *

DEBUG = False

SECRET_KEY = config('SECRET_KEY')



ALLOWED_HOSTS = ['regonwye.herokuapp.com',]




try:
    from .local import *
except ImportError:
    pass
