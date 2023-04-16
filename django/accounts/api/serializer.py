from rest_framework import serializers
from django.contrib.auth.models import User
from django.contrib.auth.hashers import make_password
from rest_framework.exceptions import APIException
from rest_framework.validators import ValidationError
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



class UserCreationSerializer(Serializer):
    first_name = serializers.SerializerMethodField()
    last_name = serializers.SerializerMethodField()
    username = serializers.CharField()
    email = serializers.EmailField()
    password1 = serializers.CharField()
    password2 = serializers.CharField()
    class Meta:
        
        fields = ["first_name", "username", "email", "password1", "password2", "date_of_birth", "bio"]

    def validate(self, attrs):

        if  User.objects.filter(username = attrs['username']).exists():
            raise UsernameExistsException(f"username {attrs['username']} already exists")
        elif User.objects.filter(email = attrs['email']).exists():
            raise EmailExistsException(f"email {attrs['email']} already exists")

        return super().validate(attrs)

    def create(self, validated_data):

        password = make_password(validated_data["password1"])

        user = User.objects.create(
            username = validated_data['username'],
            email = validated_data['email'],
            password = password,
            first_name = validated_data["first_name"],
            last_name = validated_data["last_name"]
        )

        user.save()

        return user

    def get_first_name(self, obj):
        return obj.user.first_name
    
    def get_last_name(self, obj):
        return obj.user.last_name

    


class FollowerSerializer(Serializer):
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
        

class EmailExistsException(ValidationError):
    pass


class UsernameExistsException(ValidationError):
    pass