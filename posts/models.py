from django.db import models
from uuid import uuid4
from django.contrib.auth.models import User


class Account(models.Model):
    id = models.UUIDField(default = uuid4, null=False, primary_key=True, editable = False, unique=True)
    first_name = models.CharField(max_length=50)
    last_name = models.CharField(max_length=50)
    email = models.EmailField(max_length=50)
    user_id = models.OneToOneField(User, on_delete=models.CASCADE, null=False, blank=False)
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


