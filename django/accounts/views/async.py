from rest_framework.decorators import api_view
from ...accounts.models import MediaProfile
from django.http import FileResponse
from django.conf import settings


#asynchronous request media profile
@api_view(['GET'])
def get_profile_image(request, id, num):
    images = MediaProfile.objects.filter(user_id = id).order_by("set_at")
    content_url = settings.USER_DEFAULT_PROFILE if not images.exists() else images[num].content_url

    image = open(content_url, 'rb')
    return FileResponse(image, content_type = 'image/jpeg')
