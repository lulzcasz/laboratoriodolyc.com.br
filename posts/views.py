from django.http import JsonResponse
from django.core.files.storage import default_storage
from django.contrib.auth.decorators import login_required
from uuid import uuid4
from posts.tasks.image import process_image
from django.utils import timezone


@login_required
def tinymce_upload_image(request):
    if request.method == 'POST' and request.FILES.get('file'):
        upload = request.FILES['file']

        date_path = timezone.now().strftime('%Y/%m/%d')

        file_path = default_storage.save(
            f"posts/content-images/{date_path}/{uuid4()}.avif", upload
        )
        file_url = default_storage.url(file_path)

        process_image.delay(file_path, 'content_image')
        
        return JsonResponse({'location': file_url})
    return JsonResponse({'error': 'Invalid request'}, status=400)
