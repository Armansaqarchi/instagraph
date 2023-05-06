from django.db import models
from uuid import uuid4

from django.contrib.auth.models import User

# Create your models here.


FR_STATUS = (
    ("True", "YES"),
    ("False", "NO"),
    ("pending", "PENDING")
)


class Account(models.Model):
    id = models.AutoField(null=False, primary_key=True, editable = False, unique=True)
    email = models.EmailField(max_length=50, unique=True)
    user = models.OneToOneField(User, on_delete=models.CASCADE, null=False, blank=False)
    date_of_birth = models.DateField(auto_now_add=True)
    bio = models.TextField(max_length=500)
    is_private = models.BooleanField(default=False)
    followers = models.PositiveBigIntegerField(default = 0)
    following = models.PositiveBigIntegerField(default = 0)
    posts = models.PositiveBigIntegerField(default = 0)
    fr_counts = models.PositiveBigIntegerField(default=0)
    

    class Meta:
        ordering = ['date_of_birth']
        db_table = 'accounts'


    def __str__(self):
        return self.user.username
    





class Follows(models.Model):
    id = models.AutoField(null=False, primary_key=True, editable = False, unique=True)
    follower = models.ForeignKey(Account, on_delete=models.CASCADE, related_name='follower_set', null=True) # temporarily True, in debugging mode
    following = models.ForeignKey(Account, on_delete=models.CASCADE, related_name='following_set', null=True)
    start_following_at = models.DateField(auto_now_add=True)

    class Meta:
        db_table = 'follows'
        ordering = ['start_following_at']

    def __str__(self):
        return self.follower + "->" + self.following


class FollowRQ(models.Model):
    id = models.AutoField(null=False, primary_key=True, editable = False, unique=True)
    sender = models.ForeignKey(Account, on_delete=models.CASCADE, null=True, related_name="sent_set") # temporarily True, in debugging mode
    recipient = models.ForeignKey(Account, on_delete=models.CASCADE, null=True, related_name="received_set")
    is_read = models.BooleanField(default=False)
    accepted = models.CharField(choices=FR_STATUS, default="PENDING", max_length=25)
    sent_at = models.DateField(auto_now_add=True)

    def __str__(self):
        return self.sender + "->" + self.recipient
    
    class Meta:
        db_table = "follow_requests"
        ordering = ["sent_at"]


class Story(models.Model):
    id = models.AutoField(null=False, primary_key=True, editable = False, unique=True)
    user_id = models.ForeignKey(Account, on_delete=models.CASCADE) 
    content_url = models.URLField(max_length=200)
    created_at = models.DateTimeField(auto_now_add=True)
    expires_at = models.DateTimeField(auto_now_add=True)        


    class Meta:
        db_table = 'stories'

    def __Str__(self):
        return self.user_id.username


class Message(models.Model):
    message_id = models.AutoField(null=False, primary_key=True, editable = False, unique=True)
    sender_id = models.ForeignKey(Account, on_delete=models.CASCADE)
    recipient_id = models.ForeignKey(Account, on_delete=models.CASCADE, related_name="recipient_set")
    content = models.TextField(max_length=600)
    sent_at = models.DateTimeField(auto_now_add=True)


    def __str__(self):
        return self.sender_id.username + " " + self.recipient_id.username
    


class Activation(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE, null=True)
    email = models.EmailField(blank=True)
    code = models.CharField(max_length=50, unique=True)
    created_at = models.DateTimeField(auto_now_add=True)


    class Meta:
        db_table = "Activation"
        ordering = ['created_at']


class MediaProfile:
    id = models.UUIDField(default = uuid4, null=False, primary_key=True, editable = False, unique=True)
    user_id = models.ForeignKey(Account, on_delete=models.CASCADE, related_name="image_set")
    content_url = models.URLField(max_length=200)
    set_at = models.DateField(auto_now_add=True)

    class Meta:
        ordering = ['set_at']
        db_table = "media_profile"