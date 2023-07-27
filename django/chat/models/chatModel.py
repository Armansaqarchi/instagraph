# Create your models here.
from django.db import models
from uuid import uuid4
from accounts.models import Account


MESSAGE_TYPE = (
    (1, "post_message"),
    (2, "text_message")
)

class Chat(models.Model):
    id = models.UUIDField(default= uuid4, null=False, primary_key=True, editable=True, unique=True)
    members = models.ManyToManyField(Account)
    
    @property
    def latest_message(self):
        self.latest_message = self.messages.last()
    

class Group(models.Model):
    chat = models.OneToOneField(Chat, on_delete=models.CASCADE)
    name = models.CharField(max_length=200)