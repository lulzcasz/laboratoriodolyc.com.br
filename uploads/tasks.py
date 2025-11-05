from celery import shared_task
import logging
from django.core.files.storage import default_storage
from django.core.files.base import File
import tempfile
import os
import subprocess
from io import BytesIO
from PIL import Image

logger = logging.getLogger(__name__)

@shared_task(bind=True)
def process_video(self, video_name):
    with tempfile.TemporaryDirectory() as temp_dir:
        try:
            input_path = os.path.join(temp_dir, os.path.basename(video_name))
            
            output_video_name_s3 = video_name.replace("raw.mp4", "processed.webm")
            
            output_path_local = os.path.join(temp_dir, os.path.basename(output_video_name_s3))

            logger.info(f"Downloading {video_name} from S3 to {input_path}")
            with default_storage.open(video_name, 'rb') as s3_file:
                with open(input_path, 'wb') as local_file:
                    local_file.write(s3_file.read())

            logger.info(f"Successfully downloaded file.")

            cmd = [
                'ffmpeg',
                '-i', input_path,
                '-vf', 'scale=1280:720:force_original_aspect_ratio=decrease',
                '-c:v', 'libvpx-vp9',
                '-crf', '30',
                '-b:v', '0',
                '-c:a', 'libopus',
                '-b:a', '128k',
                '-r', '30',
                output_path_local
            ]

            logger.info(f"Starting ffmpeg processing for: {input_path}")
            result = subprocess.run(
                cmd, 
                capture_output=True, 
                text=True, 
                check=True
            )
            logger.info(f"ffmpeg STDOUT: {result.stdout}")

            logger.info(f"Uploading processed file to S3: {output_video_name_s3}")
            with open(output_path_local, 'rb') as processed_file:
                default_storage.save(output_video_name_s3, File(processed_file))

            logger.info(f"Successfully processed and uploaded: {output_video_name_s3}")

            return output_video_name_s3

        except subprocess.CalledProcessError as e:
            logger.error(f"ffmpeg processing failed for {video_name}.")
            logger.error(f"ffmpeg STDERR: {e.stderr}")
            raise self.retry(exc=e, countdown=300)
            
        except Exception as e:
            logger.error(f"An error occurred processing {video_name}: {e}")
            raise self.retry(exc=e, countdown=300)

@shared_task(bind=True)
def delete_videos(self, video_name):
    default_storage.delete(video_name)
    default_storage.delete(video_name.replace("raw.mp4", "processed.webm"))


@shared_task(bind=True)
def process_image(self, image_name, max_size=(1280, 720), quality=85):
    logger.info(f"Starting image processing for: {image_name}")

    output_name_s3 = image_name.replace("raw.png", "processed.webp")

    output_buffer = BytesIO()

    try:
        logger.info(f"Opening {image_name} from default storage.")
        with default_storage.open(image_name, 'rb') as s3_file:
            img = Image.open(s3_file)

            logger.info(f"Original size: {img.size}, mode: {img.mode}")

            if img.mode not in ("RGB", "RGBA"):
                img = img.convert("RGB")
                logger.info(f"Converted image mode to RGB.")

            img.thumbnail(max_size, Image.Resampling.LANCZOS)
            logger.info(f"Resized to: {img.size}")

            img.save(output_buffer, "WEBP", quality=quality, method=6)
        
        output_buffer.seek(0)
        
        logger.info(f"Uploading processed file to S3: {output_name_s3}")
        saved_name = default_storage.save(output_name_s3, File(output_buffer))
        
        logger.info(f"Successfully processed and uploaded: {saved_name}")
        return saved_name

    except FileNotFoundError:
        logger.error(f"File not found in storage: {image_name}")

    except IOError as e:
        logger.error(f"Pillow (IOError) failed for {image_name}: {e}")

    except Exception as e:
        logger.error(f"An error occurred processing {image_name}: {e}")
        logger.exception(f"Traceback for {image_name}:")

        raise self.retry(exc=e, countdown=300)
    
    finally:
        output_buffer.close()

@shared_task(bind=True)
def delete_images(self, image_name):
    default_storage.delete(image_name)
    default_storage.delete(image_name.replace("raw.png", "processed.webp"))
