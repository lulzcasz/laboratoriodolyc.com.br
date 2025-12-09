from django.db.models.signals import post_save
from django.dispatch import receiver
from django.db import transaction
from products.tasks.image import process_image
from products.models import Product


@receiver(post_save)
def image_post_save(sender, instance, created, **kwargs):
    if not isinstance(instance, Product):
        return
    
    if getattr(instance, '_image_changed', False):
        transaction.on_commit(
            lambda: process_image.delay(instance.image.name)
        )
