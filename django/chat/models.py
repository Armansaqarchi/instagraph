from django.db import models
from django.contrib.contenttypes.models import ContentType
from django.contrib.contenttypes.fields import GenericForeignKey
from accounts.models import Account
from uuid import uuid4
from posts.models import Post

# Create your models here.

MESSAGE_TYPE = (
    (1, "post_message"),
    (2, "text_message")
)


class Group(models.Model):

    group_id = models.UUIDField(default=uuid4, null=False, primary_key=True, editable=True, unique=True)
    @property
    def get_messages(self):
        try:
            return TextMessage.objects.filter(content_type= Group, object_id= self.group_id).order_by('created_at')
        except TextMessage.DoesNotExist:
            return None

class BaseMessage(models.Model):
    message_id = models.AutoField(null=False, editable=False, primary_key=True)
    message_type = models.CharField(choices=MESSAGE_TYPE, max_length=50)
    is_read = models.BooleanField()
    sender_id = models.ForeignKey(Account, on_delete=models.CASCADE)
    content_type = models.ForeignKey(ContentType, on_delete= models.CASCADE, related_name= "recipient_set",
                                        limit_choices_to= {"model_in" : (Account, Group)})
    sent_at = models.DateTimeField(auto_now_add=True)
    object_id = models.PositiveIntegerField()
    recipient = GenericForeignKey('content_type', 'object_id')
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


