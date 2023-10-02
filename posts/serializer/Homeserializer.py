from rest_framework import serializers
from ..models import Post
from collections import OrderedDict
from accounts.models import Story
from django.contrib.auth.models import User
from exceptions.exceptions import *
from django.db import transaction
from ..models import Like
from ..models import MediaPost
from taggit.managers import TaggableManager
from taggit.serializers import TagListSerializerField


class PostSerializer(serializers.Serializer):
    medias = serializers.ListField(child = serializers.ImageField(), allow_empty = True)
    description = serializers.CharField()
    location = serializers.CharField()
    user = serializers.IntegerField(required = True, min_value=0)
    tags = TagListSerializerField()


    def validate_user(self, user):
        if not User.objects.filter(pk = user).exists():
            raise BadRequestException("no such user", code = "invalid_user_pk")
        return user

    @transaction.atomic
    def create(self, validated_data):
        post = Post.objects.create(
            description = validated_data.get("description", ""),
            location = validated_data.get("location", ""),
            user = validated_data.get("user"),
            tags = validated_data.get("tags", None)
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
    
    def update(self, validated_data, instance):
        instance.description = getattr(validated_data, "description", instance.description)
        instance.location = getattr(validated_data, "location", instance.location)
        if hasattr(validated_data, "tags"):
            instance.tags.set(getattr(validated_data, "tags", instance.tags))
        instance.save()
        



            
class StorySerializer(serializers.ModelSerializer):
    class Meta:
        model = Story
        fields = "__all__"


class LikesSerializer(serializers.Serializer):
    """
    just a class for representing likes.
    any Like object is different from its representation
    thus, the only application of this class is to represent the like object
    """

    user = serializers.IntegerField()
    post = serializers.UUIDField()

    def create(self, validated_data):

        like, created = Like.objects.get_or_create(
            user_id = validated_data["user"],
            post_id = str(validated_data["post"])
        )
        if not created:
            raise AlreadyExistsException("you have already liked this post", code = "post_already_liked")
        return like
         

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
    but when it comes to update or any kind of edit,
    there is only one attribute that is editable which is content
    """

    content = serializers.CharField(source = "content")

    def update(self, instance, validated_data):
        instance.content = validated_data.get("content", instance.content)
        instance.save()
        return instance 


    def to_representation(self, comment):
        """
        to_representation the comment
        comment.user refers to the account associated with this comment
        and comment.user.user referes to the user associated to the comment,
        as you can access any user with having its associated user
        """
        ret = OrderedDict()
        ret["user_id"] = comment.user.user.id
        ret["username"] = comment.user.user.username
        ret["firstname"] = comment.user.user.first_name
        ret["lastname"] = comment.user.user.last_name
        ret["is_private"] = comment.user.is_private
        ret["date"] = comment.commented_at
        ret["content"] = comment.content

        return ret
        
    
