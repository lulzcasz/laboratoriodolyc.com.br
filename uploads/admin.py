from django.contrib import admin
from uploads.models import Image, Video
from django.utils.html import format_html


@admin.register(Image)
class ImageAdmin(admin.ModelAdmin):
    list_display = ['post', 'kind', 'link', 'processed']
    list_filter = ('post', 'kind', 'processed')

    def link(self, obj):
        return format_html('<a href="{}" target="_blank">link</a>', obj.image.url)


@admin.register(Video)
class VideoAdmin(admin.ModelAdmin):
    list_display = ['post', 'link', 'processed']
    list_filter = ('post', 'processed')

    def link(self, obj):   
        return format_html('<a href="{}" target="_blank">link</a>', obj.video.url)
