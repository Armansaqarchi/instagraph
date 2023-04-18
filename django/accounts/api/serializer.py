from rest_framework import serializers
from django.contrib.auth.models import User
from django.contrib.auth.hashers import make_password
from rest_framework.exceptions import APIException
from rest_framework.validators import ValidationError
from collections import OrderedDict
from rest_framework.fields import SkipField
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
        



class UserCreationSerializer(Serializer):
    first_name = serializers.CharField()
    last_name = serializers.CharField()
    username = serializers.CharField()
    email = serializers.EmailField()
    password = serializers.CharField()

    class Meta:
        
        fields = ["first_name", "username", "email", "password1", "password2", "date_of_birth", "bio"]

    def validate(self, attrs):

        if  User.objects.filter(username = attrs['username']).exists():
            raise UsernameExistsException(f"username {attrs['username']} already exists")
        elif User.objects.filter(email = attrs['email']).exists():
            raise EmailExistsException(f"email {attrs['email']} already exists")

        return super().validate(attrs)

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