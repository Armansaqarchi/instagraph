from django.db import models
from chat.models.chatModel import Chat, MESSAGE_TYPE
from uuid import uuid4
from posts.models import Post

class BaseMessage(models.Model):
    message_id = models.AutoField(null=False, editable=False, primary_key=True)
    message_type = models.CharField(choices=MESSAGE_TYPE, max_length=50)
    chat = models.ForeignKey(Chat, on_delete=models.CASCADE)
    is_read = models.BooleanField()
    sent_at = models.DateTimeField(auto_now_add=True)
    class Meta:
        indexes = [
            models.Index(fields= ['object_id', 'content_type']),
            models.Index(fields= ['sender_id', 'object_id', 'content_type']),
            models.Index(fields= ['sender_id', 'object_id', 'content_type', 'sent_at'])
        ]

class TextMessage(models.Model):
    message_id = models.OneToOneField(BaseMessage, on_delete=models.CASCADE)
    content = models.TextField(max_length=600)


    def __str__(self):
        return self.sender_id.username + " " + self.recipient_id.username

class PostMessage(models.Model):
    message_id = models.OneToOneField(BaseMessage, on_delete=models.CASCADE)
    post_id = models.ForeignKey(Post, on_delete=models.CASCADE)







