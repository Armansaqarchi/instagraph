from django.db import models
from uuid import uuid4

from django.contrib.auth.models import User

# Create your models here.


class Account(models.Model):
    id = models.UUIDField(default = uuid4, null=False, primary_key=True, editable = False, unique=True)
    username = models.CharField(max_length = 50, null=True, unique=True, editable=True)
    first_name = models.CharField(max_length=50)
    last_name = models.CharField(max_length=50)
    email = models.EmailField(max_length=50, unique=True)
    user = models.OneToOneField(User, on_delete=models.CASCADE, null=False, blank=False)
    date_of_birth = models.DateField(auto_now_add=True)
    bio = models.TextField(max_length=500)
    followers = models.PositiveBigIntegerField(default = 0)
    following = models.PositiveBigIntegerField(default = 0)
    posts = models.PositiveBigIntegerField(default = 0)
    

    class Meta:
        ordering = ['date_of_birth']
        db_table = 'accounts'




class Follows(models.Model):
    id = models.UUIDField(default = uuid4, null=False, primary_key=True, editable = False, unique=True)
    follower_id = models.ForeignKey(Account, on_delete=models.CASCADE, related_name='follower_id', null=True) #temporarily True, in debugging mode
    following_id = models.ForeignKey(Account, on_delete=models.CASCADE, related_name='following_id', null=True)
    start_following_at = models.DateField(auto_now_add=True)

    class Meta:
        db_table = 'follows'
        ordering = ['start_following_at']



class Story(models.Model):
    id = models.UUIDField(default = uuid4, null=False, primary_key=True, editable = False, unique=True)
    user_id = models.ForeignKey(Account, on_delete=models.CASCADE) 
    content_url = models.URLField(max_length=200)
    created_at = models.DateTimeField(auto_now_add=True)
    expires_at = models.DateTimeField(auto_now_add=True)        


    class Meta:
        db_table = 'stories'