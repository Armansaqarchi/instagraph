from rest_framework import serializers
from django.contrib.auth.models import User
from django.contrib.auth.hashers import make_password
from rest_framework.exceptions import APIException
from rest_framework.validators import ValidationError
from collections import OrderedDict
from rest_framework.fields import SkipField
from ..models import FollowRQ
from chat.models.messageModel import BaseMessage
from accounts.models import MediaProfile
from exceptions.exceptions import *
from os import path
from django.conf import settings
from rest_framework.serializers import(
    Serializer,
    ModelSerializer
)
from ..models import (
    Account,
    Follows
)

class AccountSerializer(ModelSerializer):
    first_name = serializers.CharField()
    last_name = serializers.CharField()
    email = serializers.EmailField()
    date_of_birth = serializers.DateField()
    bio = serializers.CharField(style={'base_template': 'textarea.html'})

    class Meta:
        model = Account
        fields = ["first_name", "last_name", "email", "date_of_birth", "bio"]

    def to_representation(self, instance):
        """
        Object instance -> Dict of primitive datatypes.
        """
    
        ret = OrderedDict()

        ret["first_name"] = instance.user.first_name
        ret["last_name"] = instance.user.last_name

        fields = self._readable_fields

        for field in fields:
            try:
                attribute = field.get_attribute(instance)
            except SkipField:
                continue
            # this function is the same as parent function but raises AttrbuteError when firstname and lastname is not found
            except AttributeError:
                continue

            if attribute is None:
                ret[field.field_name] = None
            else:
                ret[field.field_name] = field.to_representation(attribute)

        return ret
        

class ProfileSerializer(Serializer):
    profile_picture = serializers.SerializerMethodField()
    firstname = serializers.SerializerMethodField()
    lastname = serializers.SerializerMethodField()
    username = serializers.SerializerMethodField()
    bio = serializers.CharField()
    followers = serializers.SerializerMethodField()
    followings = serializers.SerializerMethodField()
    posts = serializers.SerializerMethodField()


    def get_profile_picture(self, object):
        try:
            serialized_profile =  MediaProfileSerializer(object.profile_images.first())
            return serialized_profile.data
        except TypeError:
            return None
    def get_firstname(self, object):

        return object.user.first_name
    def get_lastname(self, object):
        return object.user.last_name
    def get_username(self, object):
        return object.user.username
    def get_followers(self, object):
        return object.following_set.count()
    def get_followings(self, object):
        return object.follower_set.count()
    def get_posts(self, object):
        return object.user_posts.count()


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
        return super().validate(attrs)\


    def create(self, validated_data):

        password = make_password(validated_data["password"])
        user = User.objects.create(
            username = validated_data['username'],
            email = validated_data['email'],
            password = password,
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

class FollowRQSerializer(Serializer):
    follows_id = serializers.IntegerField(source="follows_id")
    follower = serializers.CharField(source="follower")
    following = serializers.CharField(source="following")
    is_private = serializers.BooleanField(source="is_private")
    class Meta:
        fields = ["follows_id", "follower", "following", "is_private"]

    def create(self, validated_data):
        follows = Follows.objects.create(
            follower = validated_data["follower"],
            following = validated_data["following"]
        )

        return follows    

   
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
        
        if self.context.get("id") is None:
            return ValidationError("no id specified")
    
    def change_password(self):
        try:
            account = Account.objects.get(self.context.get("id"))
        except Account.DoesNotExist:
            raise NotFoundException("No such user")
        account.set_password(self.new_password)

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