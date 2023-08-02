from django.contrib.contenttypes.models import ContentType
from django.contrib.contenttypes.fields import GenericForeignKey
from django.db import models
from uuid import uuid4
from django.conf import settings
from django.contrib.auth.models import User
from rest_framework_simplejwt.tokens import RefreshToken
from datetime import datetime, timedelta


class Account(models.Model):

    GENDER = (
        ("Male", "Male"),
        ("Female", "Female"),
        ("Unknown", "Prefer not to say")
    )
    
    id = models.AutoField(null=False, primary_key=True, editable = False, unique=True)
    user = models.OneToOneField(User, on_delete=models.CASCADE, null=False, blank=False, unique=True)
    date_of_birth = models.DateField(auto_now_add=True)
    bio = models.TextField(max_length=500)
    gender = models.CharField(max_length=100, choices=GENDER, default="Prefer not to say")
    is_private = models.BooleanField(default=False)
    followers = models.PositiveBigIntegerField(default = 0)
    following = models.PositiveBigIntegerField(default = 0)
    last_seen_posts = models.DateField(auto_now_add=True, null=False)


    @property
    def token(self):
        return RefreshToken.for_user(self.user)

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

        # there are 2 constraints so far, one for checking wheater follower not quals following!
        # and second, to check that only one pair of (follower, following) exists at a time
        constraints = [
            models.CheckConstraint(check=~models.Q(follower=models.F('following')), name='dont_follow_yourself'),
            models.UniqueConstraint(fields=["follower", "following"], name="only_follow_once")
        ]

    def __str__(self):
        return self.follower.user.username + "->" + self.following.user.username


class FollowRQ(models.Model):

    FR_STATUS = (
    ("True", "YES"),
    ("False", "NO"),
    ("pending", "PENDING")
    )


    id = models.UUIDField(default=uuid4, null=False, primary_key=True, editable = False, unique=True)
    sender = models.ForeignKey(Account, on_delete=models.CASCADE, null=True, related_name="sent_set") # temporarily True, in debugging mode
    recipient = models.ForeignKey(Account, on_delete=models.CASCADE, null=True, related_name="received_set")
    is_read = models.BooleanField(default=False)
    accepted = models.CharField(choices=FR_STATUS, default="PENDING", max_length=25)
    sent_at = models.DateField(auto_now_add=True)

    def __str__(self):
        return self.sender.user.username + "->" + self.recipient.user.username
    
    class Meta:
        db_table = "follow_requests"
        ordering = ["sent_at"]
        constraints = [
            models.CheckConstraint(check=~models.Q(sender = models.F('recipient')), name="dont request yourself")
        ]


class Story(models.Model):
    id = models.AutoField(null=False, primary_key=True, editable = False, unique=True)
    user_id = models.ForeignKey(Account, on_delete=models.CASCADE, related_name="account_stories") 
    content_url = models.ImageField(max_length=200, default = settings.USER_DEFAULT_STORY, upload_to=settings.STORY_UPLOAD_DIR)
    created_at = models.DateTimeField(auto_now_add=True)
    expires_at = models.DateTimeField(auto_now_add=True)        


    class Meta:
        db_table = 'stories'

    def __str__(self):
        return self.user_id.user.username
    

class Activation(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE, null=True)
    email = models.EmailField(blank=True)
    code = models.CharField(max_length=50, unique=True)
    created_at = models.DateTimeField(auto_now_add=True)

    class Meta:
        db_table = "Activation"
        ordering = ['created_at']


class MediaProfile(models.Model):
    id = models.UUIDField(default = uuid4, null=False, primary_key=True, editable = False, unique=True)
    user = models.ForeignKey(Account, on_delete=models.CASCADE, related_name="profile_images")
    profile_image = models.ImageField(max_length=200, default = settings.USER_DEFAULT_PROFILE , null=True, upload_to=settings.PROFILE_UPLOAD_DIR)
    set_at = models.DateField(auto_now_add=True)

    class Meta:
        db_table = "profile"
        ordering = ['set_at']


