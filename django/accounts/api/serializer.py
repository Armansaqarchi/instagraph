from rest_framework.serializers import ModelSerializer
from rest_framework import serializers
from ..models import Account


class AccountSerializer(ModelSerializer):
    first_name = serializers.CharField(source="Firstname")
    last_name = serializers.CharField(source="Lastname")
    email = serializers.EmailField(source="Email")
    date_of_birth = serializers.DateField(source="Date of birth")
    bio = serializers.CharField(style={'base_template': 'textarea.html'}, source="Bio")

    class Meta:
        model = Account
        fields = ["first_name", "last_name", "email", "date_of_birth", "bio"]
        