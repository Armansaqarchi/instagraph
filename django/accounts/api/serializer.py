from rest_framework import serializers
from django.contrib.auth.models import User
from collections import OrderedDict
from rest_framework.validators import ValidationError
from ..models import FollowRQ
from chat.models.messageModel import BaseMessage
from accounts.models import MediaProfile
from exceptions.exceptions import *
from rest_framework.fields import Field
from django.conf import settings
from rest_framework.serializers import(
    Serializer,
    ModelSerializer
)
from ..models import (
    Account,
    Follows
)



class ProfileViewSerializer(Serializer):
    """
    the class only needs 'to_representation' method,
    this is for showing profile to whoever authorized to view
    """

    profile_picture = serializers.SerializerMethodField()
    firstname = serializers.SerializerMethodField()
    lastname = serializers.SerializerMethodField()
    username = serializers.SerializerMethodField()
    bio = serializers.CharField()
    followers = serializers.SerializerMethodField()
    followings = serializers.SerializerMethodField()
    posts = serializers.SerializerMethodField()

    def to_representation(self, instance):
        ret = OrderedDict()
        ret["firstname"] = instance.user.firstname
        ret["lastname"] = instance.user.lastname
        ret["username"] = instance.user.username
        ret["bio"] = instance.bio
        ret["followers"] = instance.followers_count
        ret["followings"] = instance.followings_count
        ret["posts"] = instance.posts_list
        ret["profile_picture"] = instance.profile_images.first().id
        return ret

class profileEditSerializer(Serializer):
    # fields here


    # validators here


    # update here


    # ro representation here





class MediaProfileSerializer(ModelSerializer):
    class Meta:
        model = MediaProfile
        exclude = ["profile_image"]

class UserSerializer(Serializer):
    first_name = serializers.CharField()
    last_name = serializers.CharField()
    username = serializers.CharField()
    email = serializers.EmailField()
    password = serializers.CharField()

    class Meta:
        fields = ["first_name", "username", "email", "password2", "date_of_birth", "bio"]

    def validate(self, attrs):
        if  User.objects.filter(username = attrs['username']).exists():
            raise UsernameExistsException()
        elif User.objects.filter(email = attrs['email']).exists():
            raise EmailExistsException()
        return super().validate(attrs)


    def create(self, validated_data):


        user = User.objects.create_user(
            username = validated_data['username'],
            email = validated_data['email'],
            password = validated_data["password"],
            first_name = validated_data["first_name"],
            last_name = validated_data["last_name"]
        )
        user.save()
        return user
    
    def update(self, instance, validated_data):
        print("dsfafsaffsa", instance)
        print(validated_data)

    def get_first_name(self, obj):
        return obj.user.first_name
    
    def get_last_name(self, obj):
        return obj.user.last_name

   
class FollowerSerializer(Serializer):
    follows_id = serializers.IntegerField(source = "id")
    follower = serializers.SerializerMethodField()
    following_image = serializers.SerializerMethodField()
    is_private = serializers.BooleanField()

    class Meta:
        fields = ('follows_id', 'following')


    def get_follower(self, obj):
        return obj.user.username
    
    def get_following_image(self, obj):
        try:
            return obj.profile_images.first().id
        except AttributeError:
            return None

class FollowingSerializer(Serializer):
    follows_id = serializers.IntegerField(source = "id")
    following = serializers.SerializerMethodField()
    following_image = serializers.SerializerMethodField()
    is_private = serializers.BooleanField()

    class Meta:
        fields = ('follows_id', 'following')


    def get_following(self, obj):
        return obj.user.username
    
    def get_following_image(self, obj):
        try:
            return obj.profile_images.first().id
        except AttributeError:
            return None
        
class PasswordChangeSerializer(Serializer):
    new_password = serializers.CharField()
    confirm_new_password = serializers.CharField()

    def validate(self, attrs):
        if attrs.get("new_password") != attrs.get("confirm_new_password"):
            raise ValidationError("password and confirm password should match")
        
        if not hasattr(self.context, id):
            return ValidationError("no id specified")
    
    def change_password(self):
        try:
            account = Account.objects.get(self.context.get("id"))
        except Account.DoesNotExist:
            raise NotFoundException("No such user")
        account.user.set_password(self.new_password)

class FollowRequestSerializer(ModelSerializer):

    class Meta:
        model = FollowRQ
        fields = "__all__"

class MessageSerializer(ModelSerializer):

    class Meta:
        model = BaseMessage
        fields = "__all__"

class EmailExistsException(Exception):
    pass


class UsernameExistsException(Exception):
    pass