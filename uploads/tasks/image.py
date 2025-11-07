from celery import shared_task
from uploads.models import Image
from django.core.files.storage import default_storage
from io import BytesIO
from PIL import Image as PILImage


@shared_task(bind=True)
def process_image(self, image_id):
    image = Image.objects.get(id=image_id)
    print(image.image.name)

    with image.image.open('rb') as old:
        new = BytesIO()

        with PILImage.open(old) as img:
            img_rgba = img.convert('RGBA')

            if image.kind == Image.Kind.POST_COVER:
                img_rgba = img_rgba.resize((1024, 576), PILImage.Resampling.LANCZOS)

            else:
                img_rgba.thumbnail((1024, 576), PILImage.Resampling.LANCZOS)
                
            img_rgba.save(new, "WEBP", quality=85, method=6)

            new.seek(0)

        image.image.save(image.image.name, new)

    image.processed = True
    image.save()


@shared_task(bind=True)
def delete_image(self, image_name):
    default_storage.delete(image_name)
