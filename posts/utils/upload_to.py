from os.path import splitext

def post_image_path(instance, filename):
    return f'posts/covers/{instance.uuid}/large.avif'
