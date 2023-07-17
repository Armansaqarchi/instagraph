from rest_framework.views import APIView
from django.http import FileResponse
from django.contrib.auth.mixins import LoginRequiredMixin
from rest_framework.response import Response
from rest_framework.permissions import BasePermission
from django.db.models import Q
from rest_framework.decorators import permission_classes
from ..models import MediaPost
from accounts.exceptions.Exceptions import *
from accounts.models import Account
from rest_framework.status import (
    HTTP_404_NOT_FOUND,
    HTTP_400_BAD_REQUEST
)

class IsFollowerOrPagePublic(BasePermission):
    def has_object_permission(self, request, view, obj):
        try:
            return not obj.user_id.is_private or obj.user_id.following_set.get(follower__id = request.user.account.id)
        except Account.DoesNotExist:
            return False
        


class AsyncPostGet(LoginRequiredMixin, APIView):

    permission_classes = [IsFollowerOrPagePublic]
    

    def get(self, request):
        try:

            num = int(request.GET.get("slide"))
            post_id = request.GET.get("id")
            media_post = MediaPost.objects.filter(Q(post_id = post_id) & Q(page_num = num)).first()
            
            self.check_object_permissions(request, media_post.post_id)
            if media_post is None:
                return Response({"message" : "no image found", "status" : "error"}, status=HTTP_404_NOT_FOUND)
            image_file = open(media_post.content_url.path, 'rb')
            return FileResponse(image_file, content_type = "image/jpeg")
        except ValueError as e:
            raise BadRequestException(str(e))
        except FileNotFoundError as e:
            return NotFoundException("No such file or stream found")







