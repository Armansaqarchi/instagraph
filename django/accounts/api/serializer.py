from rest_framework import serializers
from ..models import Account
from django.contrib.auth.models import User
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
    username = serializers.CharField(source="Firstname")
    email = serializers.EmailField(source="Email")
    password1 = serializers.CharField(source="Password")
    password2 = serializers.CharField(source="Confirm Password")
    class Meta:
        
        fields = ["first_name", "username", "email", "password1", "password2", "date_of_birth", "bio"]

    def create(**validated_data):
        User.objects.create(**validated_data)
        

