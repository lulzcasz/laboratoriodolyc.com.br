from .base import *

DEBUG = False

AWS_S3_REGION_NAME = getenv("AWS_S3_REGION_NAME")

STORAGES["staticfiles"].update(
    {
        "BACKEND": "storages.backends.s3.S3Storage",
        "OPTIONS": {
            "location": "staticfiles",
        },
    }
)

CSRF_TRUSTED_ORIGINS = getenv('DJANGO_CSRF_TRUSTED_ORIGINS').split(',')
