from rest_framework import serializers
from ..models import Post
from accounts.models import Story
from django.contrib.auth.models import User
from exceptions.exceptions import *
from django.db import transaction
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