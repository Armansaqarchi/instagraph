from rest_framework import serializers
from ..models import Post
from collections import OrderedDict
from accounts.models import Story
from django.contrib.auth.models import User
from exceptions.exceptions import *
from django.db import transaction
from rest_framework.serializers import ListSerializer
from ..models import MediaPost


class PostSerializer(serializers.Serializer):
    medias = serializers.ListField(child = serializers.ImageField(), allow_empty = True)
    description = serializers.CharField()
    location = serializers.CharField()
    user = serializers.IntegerField(required = True, min_value=0)

    def validate_user(self, user):
        if not User.objects.filter(pk = user).exists():
            raise BadRequestException("no such user", code = "invalid_user_pk")
        return user

    @transaction.atomic
    def create(self, validated_data):
        post = Post.objects.create(
            description = validated_data.get("description", ""),
            location = validated_data.get("location", ""),
            user = validated_data.get("user")
        )
        medias = validated_data.get("medias", None)

        if not medias:
            return
        
        page = 0
        for media in medias:
            page+=1
            MediaPost.objects.create(
                post_id = post.id,
                content_url = media,
                page_num = page
            )
            
class StorySerializer(serializers.ModelSerializer):
    class Meta:
        model = Story
        fields = "__all__"


class LikesSerializer(serializers.Serializer):
    """
    just a class for representing likes.
    any Like object has so much difference than its representation
    thus, the only application of this class is to represent the like object
    """

    def to_representation(self, like):
        account = like.user
        ret = OrderedDict()
        ret["user_id"] = account.id
        ret["username"] = account.user.username
        ret["firstname"] = account.user.first_name
        ret["lastname"] = account.user.last_name
        ret["is_private"] = account.is_private
        ret["has_user_followed"] = self.get_has_user_followed(account=account)
        ret["date"] = like.liked_at


        return ret
    
    def get_has_user_followed(self, account):
        """
        checks whether the viewer is already following the account
        when initializing this class, viewer's account must be set in the context
        """
        account = self.context["account"]
        return account.followings_list.filter(id = account.id).exists()
    

class CommentSerializer(serializers.Serializer):
    """
    just like the Like object,
    the only use of this class is to represent the comment.
    any comment has its username, user_id, content for comment
    """

    def to_representation(self, comment):
        ret = OrderedDict()
        ret["user_id"] = comment.user.id
        ret["username"] = comment.user.username
        ret["firstname"] = comment.user.first_name
        ret["lastname"] = comment.user.last_name
        ret["is_private"] = comment.user.account.is_private
        ret["date"] = comment.commented_at
        ret["content"] = comment.content
        
    
