from rest_framework import serializers
from .models.chatModel import GroupChat, Chat

class GroupChatSerializer(serializers.ModelSerializer):

    class Meta:
        model = GroupChat


class ChatListSerializer(serializers.ModelSerializer):
    """
    internal model attributes
    """
    group = GroupChatSerializer(required = True)
    

        