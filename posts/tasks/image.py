import os
import subprocess
import tempfile

from celery import shared_task
from django.core.files.base import ContentFile
from django.core.files.storage import default_storage
from PIL import Image


@shared_task(bind=True)
def process_image(self, image_name, kind):
    if kind == "cover":
        directory = os.path.dirname(image_name)

        large_width, large_height, large_crf = 1200, 630, 12

        with tempfile.NamedTemporaryFile(delete=True) as raw_input:
            with default_storage.open(image_name, "rb") as f:
                raw_input.write(f.read())
            raw_input.flush()

            with tempfile.NamedTemporaryFile(
                suffix=".avif", delete=True
            ) as large_output:

                subprocess.run(
                    [
                        "ffmpeg",
                        "-y",
                        "-i",
                        raw_input.name,
                        "-vf",
                        f"scale='if(lt(iw/ih,{large_width}/{large_height}),{large_width},-2)':'if(lt(iw/ih,{large_width}/{large_height}),-2,{large_height})',crop={large_width}:{large_height}",
                        "-pix_fmt",
                        "yuva420p",
                        "-c:v",
                        "libaom-av1",
                        "-still-picture",
                        "1",
                        "-crf",
                        str(large_crf),
                        large_output.name,
                    ],
                    check=True,
                )

                with open(large_output.name, "rb") as f:
                    processed_content = ContentFile(f.read())
                    if default_storage.exists(image_name):
                        default_storage.delete(image_name)

                    default_storage.save(image_name, processed_content)

                sub_versions = {
                    "medium": (600, 315, 4),
                    "small": (400, 210, 3),
                }

                for suffix, (width, height, crf) in sub_versions.items():
                    new_filename = os.path.join(directory, f"{suffix}.avif")

                    with tempfile.NamedTemporaryFile(
                        suffix=".avif", delete=True
                    ) as sub_output:
                        subprocess.run(
                            [
                                "ffmpeg",
                                "-y",
                                "-i",
                                large_output.name,
                                "-vf",
                                f"scale={width}:{height}",
                                "-pix_fmt",
                                "yuva420p",
                                "-c:v",
                                "libaom-av1",
                                "-still-picture",
                                "1",
                                "-crf",
                                str(crf),
                                sub_output.name,
                            ],
                            check=True,
                        )

                        with open(sub_output.name, "rb") as f:
                            content = ContentFile(f.read())
                            if default_storage.exists(new_filename):
                                default_storage.delete(new_filename)
                            default_storage.save(new_filename, content)

    elif kind == "content_image":
        image_url = default_storage.url(image_name)
        with tempfile.NamedTemporaryFile(suffix=".avif", delete=True) as temp_output:
            with default_storage.open(image_name, "rb") as old:
                with Image.open(old) as img:
                    if getattr(img, "is_animated", False):
                        subprocess.run(
                            [
                                "ffmpeg",
                                "-y",
                                "-i",
                                image_url,
                                "-c:v",
                                "libsvtav1",
                                "-crf",
                                "38",
                                "-r",
                                "15",
                                "-preset",
                                "2",
                                "-vf",
                                "scale='min(1024,iw)':576:force_original_aspect_ratio=decrease",
                                temp_output.name,
                            ],
                            check=True,
                        )
                    else:
                        subprocess.run(
                            [
                                "ffmpeg",
                                "-y",
                                "-i",
                                image_url,
                                "-vf",
                                "scale='min(1024,iw)':'min(576,ih)':force_original_aspect_ratio=decrease, scale='min(1024,iw)':'min(576,ih)', scale='trunc(iw/2)*2':'trunc(ih/2)*2'",
                                "-pix_fmt",
                                "yuva420p",
                                "-c:v",
                                "libaom-av1",
                                "-still-picture",
                                "1",
                                "-crf",
                                "15",
                                temp_output.name,
                            ],
                            check=True,
                        )

            with open(temp_output.name, "rb") as f:
                processed_content = ContentFile(f.read())
                default_storage.delete(image_name)
                default_storage.save(image_name, processed_content)
