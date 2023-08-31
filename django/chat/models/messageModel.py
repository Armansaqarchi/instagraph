from django.db import models
from chat.models.chatModel import Chat
from accounts.models import Account
from posts.models import Post

class BaseMessage(models.Model):

    sender = models.ForeignKey(Account, editable=False, on_delete=models.DO_NOTHING)
    message_id = models.AutoField(null=False, editable=False, primary_key=True)
    chat = models.ForeignKey(Chat, on_delete=models.CASCADE, related_name="messages")
    is_read = models.BooleanField(default=False)
    sent_at = models.DateTimeField(auto_now_add=True)
    class Meta:
        indexes = [
            models.Index(fields= ['chat'])
        ]

class TextMessage(models.Model):
    base_message = models.OneToOneField(BaseMessage, on_delete=models.CASCADE)
    content = models.TextField(max_length=600)

    def __str__(self):
        return self.sender_id.username + " " + self.recipient_id.username

class PostMessage(models.Model):
    base_message = models.OneToOneField(BaseMessage, on_delete=models.CASCADE)
    post_id = models.ForeignKey(Post, on_delete=models.CASCADE)







