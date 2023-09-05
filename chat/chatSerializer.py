from rest_framework import serializers
from .models.messageModel import BaseMessage, TextMessage
from collections import OrderedDict

class MessageSerializer(serializers.ModelSerializer):

    class Meta:
        model = TextMessage
        fields = "__all__"

    def to_representation(self, instance):
        """
        typically, a message must have content, user_id, username and the time message received
        """
        
        ret = OrderedDict()
        ret["content"] = instance.content
        ret["date"] = str(instance.base_message.sent_at)
        ret["user_id"] = instance.base_message.sender.id
        ret["username"] = instance.base_message.sender.user.username
        return ret
    

class ChatMessageSerializer(serializers.Serializer):

    def to_representation(self, instance):
        serialized_messages = [MessageSerializer(instance = message.textmessage).data for message in instance]
        return {"message" : serialized_messages}
        