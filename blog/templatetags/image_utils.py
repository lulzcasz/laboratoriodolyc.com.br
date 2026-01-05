from os.path import dirname
from django import template
from django.core.files.storage import default_storage

register = template.Library()

@register.filter
def variant(image_field, size):
    return default_storage.url(f"{dirname(image_field.name)}/{size}.avif")
