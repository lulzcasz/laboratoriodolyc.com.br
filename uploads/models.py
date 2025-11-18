from uuid import uuid4

from django.db.models import (
    CASCADE,
    CharField,
    DateTimeField,
    FileField,
    ForeignKey,
    ImageField,
    Model,
    TextChoices,
    UUIDField,
)
from uploads.utils.upload_to import (
    post_image_processed_path,
    post_image_source_path,
    post_video_processed_path,
    post_video_source_path,
)


class AbstractMedia(Model):
    uuid = UUIDField(default=uuid4, editable=False, unique=True, db_index=True)
    post = ForeignKey("posts.Post", CASCADE)
    uploaded_at = DateTimeField(auto_now_add=True)

    class Meta:
        abstract = True

    def __str__(self):
        return str(self.uuid)


class Image(AbstractMedia):
    class Kind(TextChoices):
        POST_COVER = "post_cover"
        POST_CONTENT_IMAGE = "post_content_image"

    source = ImageField("fonte", upload_to=post_image_source_path, max_length=128)
    processed = ImageField(
        upload_to=post_image_processed_path, max_length=128, blank=True,
    )
    post = ForeignKey("posts.Post", CASCADE, related_name="cover_images")
    kind = CharField(max_length=20, choices=Kind.choices)


class Video(AbstractMedia):
    source = FileField(upload_to=post_video_source_path, max_length=128)
    processed = FileField(
        upload_to=post_video_processed_path, max_length=128, blank=True,
    )
    post = ForeignKey("posts.Post", CASCADE, related_name="content_videos")
