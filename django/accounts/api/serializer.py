from rest_framework import serializers
from ..models import Account
from django.contrib.auth.models import User
from rest_framework.exceptions import APIException
from rest_framework.serializers import(
    Serializer,
    ModelSerializer
)


class AccountSerializer(ModelSerializer):
    first_name = serializers.CharField(source="Firstname")
    last_name = serializers.CharField(source="Lastname")
    email = serializers.EmailField(source="Email")
    date_of_birth = serializers.DateField(source="Date of birth")
    bio = serializers.CharField(style={'base_template': 'textarea.html'}, source="Bio")

    class Meta:
        model = Account
        fields = ["first_name", "last_name", "email", "date_of_birth", "bio"]
        


class UserCreationSerializer(Serializer):
    first_name = serializers.CharField(source="Firstname")
    last_name = serializers.CharField(source="Lastname")
    username = serializers.CharField(source="Username")
    email = serializers.EmailField(source="Email")
    password1 = serializers.CharField(source="Password")
    password2 = serializers.CharField(source="Confirm Password")
    class Meta:
        
        fields = ["first_name", "username", "email", "password1", "password2", "date_of_birth", "bio"]

    def create(self, validated_data):


        if  User.objects.filter(username = validated_data['Username']).exists():
            raise UsernameExistsException
        elif User.objects.filter(email = validated_data['Email']).exists():
            raise EmailExistsException
        

        user = User.objects.create(
            username = validated_data['Username'],
            email = validated_data['Email'],
            password = validated_data['Password'],
            first_name = validated_data["Firstname"],
            last_name = validated_data["Lastname"]
        )

        

        return user
        


class EmailExistsException(APIException):
    pass


class UsernameExistsException(APIException):
    pass