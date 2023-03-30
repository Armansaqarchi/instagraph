from django.db import models
from uuid import uuid4
from accounts.models import Account



class Post(models.Model):
    id = models.UUIDField(default = uuid4, null=False, primary_key=True, editable = False, unique=True)
    user_id = models.ForeignKey(Account, on_delete=models.CASCADE)
    description = models.CharField(max_length=500)
    likes = models.PositiveBigIntegerField(default = 0)
    comments = models.PositiveBigIntegerField(default = 0)
    created_at = models.DateTimeField(auto_now_add=True)
    location = models.CharField(max_length=50)
    class Meta:
        db_table = 'posts'


class Like(models.Model):
    id = models.UUIDField(default = uuid4, null=False, primary_key=True, editable = False, unique=True)
    user_id = models.ForeignKey(Account, on_delete=models.CASCADE)
    post_id = models.ForeignKey(Post, on_delete=models.CASCADE, related_name='posts')
    like_at = models.DateField(auto_now_add=True)

    class Meta:
        db_table = 'likes'
        ordering = ['like_at']




class Comment(models.Model):
    id = models.UUIDField(default = uuid4, null=False, primary_key=True, editable = False, unique=True)
    sender_id = models.ForeignKey(Account, on_delete=models.CASCADE)
    post_id = models.ForeignKey(to = Post, on_delete=models.CASCADE, related_name="comment_post")
    content = models.CharField(max_length=300)
    likes_count = models.PositiveBigIntegerField(default = 0)
    created_at = models.DateField(auto_now_add=True)    

    class Meta:
        db_table = 'comments'

