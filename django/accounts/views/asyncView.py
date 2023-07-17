from rest_framework.decorators import api_view
from models import MediaProfile, MediaStory
from django.http import FileResponse
from django.conf import settings
from rest_framework.response import Response
from django.db.models import Q
from ..exceptions.Exceptions import *
from rest_framework.status import (
     HTTP_400_BAD_REQUEST,
     HTTP_200_OK,
     HTTP_404_NOT_FOUND
)


#asynchronous request media profile
@api_view(['GET'])
def get_profile_image(request, id, num):
    images = MediaProfile.objects.filter(user_id = id).order_by("set_at")
    content_url = settings.USER_DEFAULT_PROFILE if not images.exists() else images[num].content_url

    image = open(content_url, 'rb')
    return FileResponse(image, content_type = 'image/jpeg')


@api_view(['GET'])
def async_story_get(request):
    try:
        num = int(request.GET.get("slide"))
        story_id = int(request.GET.get("id"))
        media_story = MediaStory.objects.filter(Q(story_id = story_id) | Q(page_num = num)).first()
        if media_story is None:
            return Response({"message" : "no image found", "status" : "success"}, status=HTTP_404_NOT_FOUND)
        image_file = open(media_story.story_image.path, 'rb')
        return FileResponse(image_file, content_type = "image/jpeg")
    except ValueError as e:
            raise BadRequestException(str(e))
    except FileNotFoundError as e:
        raise NotFoundException("No such file or stream found")