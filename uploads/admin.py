from django.contrib import admin
from uploads.models import Video, Image
from django.utils.html import format_html


@admin.register(Video)
class VideoAdmin(admin.ModelAdmin):
    fields = ('uuid', 'video', 'processed_video_link')
    readonly_fields = ('uuid', 'processed_video_link')

    def processed_video_link(self, obj):
        processed_url = obj.get_processed_video_url()
        
        return format_html(
            '<a href="{url}" target="_blank">{display_text}</a>', 
            url=processed_url,
            display_text=processed_url.replace('/media/', '.../')
        )

    processed_video_link.short_description = 'Processed Video URL'


@admin.register(Image)
class ImageAdmin(admin.ModelAdmin):
    fields = ('uuid', 'image', 'processed_image_link')
    readonly_fields = ('uuid', 'processed_image_link')

    def processed_image_link(self, obj):
        processed_url = obj.get_processed_image_url()
        
        return format_html(
            '<a href="{url}" target="_blank">{display_text}</a>', 
            url=processed_url,
            display_text=processed_url.replace('/media/', '.../')
        )

    processed_image_link.short_description = 'Processed Image URL'
