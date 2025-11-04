from celery import shared_task
import logging
from django.core.files.storage import default_storage

logger = logging.getLogger(__name__)

@shared_task(bind=True)
def process_video(self, video_name):
    print(default_storage.url(video_name))
