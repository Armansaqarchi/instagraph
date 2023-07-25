from rest_framework import serializers
from .models.chatModel import Group, Chat

class GroupChatSerializer(serializers.ModelSerializer):

    class Meta:
        model = Group


class ChatListSerializer(serializers.ModelSerializer):
    """
    internal model attributes
    """
    group = GroupChatSerializer(required = True)
    

        