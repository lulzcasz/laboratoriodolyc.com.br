from django.db.models.signals import post_save, post_delete
from django.dispatch import receiver
from django.db import transaction
from uploads.models import Video, Image
from uploads.tasks import process_video, delete_videos, process_image, delete_images


@receiver(post_save, sender=Video)
def video_post_save(sender, instance, created, **kwargs):
    if created:
        print(f"New video saved: {instance.uuid}. Queuing processing task.")
        
        transaction.on_commit(lambda: process_video.delay(instance.video.name))


@receiver(post_delete, sender=Video)
def video_post_delete(sender, instance, **kwargs):
    if instance.video:
        print(f"{instance.uuid}. Queuing processing task.")
        
        transaction.on_commit(lambda: delete_videos.delay(instance.video.name))


@receiver(post_save, sender=Image)
def image_post_save(sender, instance, created, **kwargs):
    if created:
        transaction.on_commit(lambda: process_image.delay(instance.image.name))


@receiver(post_delete, sender=Image)
def image_post_delete(sender, instance, **kwargs):
    if instance.image:
        print(f"{instance.uuid}. Queuing processing task.")
        
        transaction.on_commit(lambda: delete_images.delay(instance.image.name))
