from django.db.models.signals import post_save
from django.dispatch import receiver
from django.db import transaction
from posts.tasks.image import process_image
from posts.models import Post


@receiver(post_save)
def cover_post_save(sender, instance, created, **kwargs):
    if not isinstance(instance, Post):
        return
    
    if getattr(instance, '_cover_changed', False):
        transaction.on_commit(lambda: process_image.delay(instance.cover.name, 'cover'))


"""@receiver(post_save, sender=Video)
def video_post_save(sender, instance, created, **kwargs):
    transaction.on_commit(lambda: process_video.delay(instance.id))"""
