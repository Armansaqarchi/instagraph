from rest_framework.decorators import api_view
from django.http import FileResponse
from rest_framework.response import Response
from django.db.models import Q
from ..models import MediaPost
from rest_framework.status import (
    HTTP_404_NOT_FOUND,
    HTTP_400_BAD_REQUEST
)

@api_view(['GET'])
def async_post_get(request):
    try:
        num = int(request.GET.get("slide"))
        post_id = request.GET.get("id")
        media_post = MediaPost.objects.filter(Q(post_id = post_id) | Q(page_num = num)).first()
        if media_post is None:
            return Response({"message" : "no image found", "status" : "error"}, status=HTTP_404_NOT_FOUND)
        image_file = open(media_post.content_url.path, 'rb')
        return FileResponse(image_file, content_type = "image/jpeg")
    except ValueError as e:
        return Response({"message" : str(e)}, status=HTTP_400_BAD_REQUEST)
    except FileNotFoundError as e:
        return Response({"message" : "something went wrong while getting the image"}, status=HTTP_404_NOT_FOUND)




