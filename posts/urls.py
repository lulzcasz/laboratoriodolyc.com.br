from django.urls import path
from posts.views import tinymce_upload_image

urlpatterns = [
    path(
        'tinymce/upload-image/<uuid:post_uuid>/',
        tinymce_upload_image, name='tinymce-upload-image',
    ),
]
