"""
File storage config
"""

from django_cleanup.signals import cleanup_pre_delete
from storages.backends.s3boto3 import S3Boto3Storage

class MediaStorage(S3Boto3Storage):
    location = 'media'

def sorl_delete(**kwargs):
    """
    Function to delete thumbnails when deleting the original photo
    """
    from sorl.thumbnail import delete
    delete(kwargs['file'])

cleanup_pre_delete.connect(sorl_delete)
