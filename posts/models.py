from django.db import models
from uuid import uuid4
from accounts.models import Account
from django.conf import settings
from taggit.managers import TaggableManager
from django.utils.translation import gettext_lazy as _

class Post(models.Model):
    id = models.UUIDField(default = uuid4, null=False, primary_key=True, editable = False, unique=True)
    user = models.ForeignKey(Account, on_delete=models.CASCADE, related_name="user_posts")
    description = models.CharField(max_length=500)
    likes = models.PositiveBigIntegerField(default = 0)
    comments = models.PositiveBigIntegerField(default = 0)
    created_at = models.DateTimeField(auto_now_add=True)
    location = models.CharField(max_length=50, null=True)
    tags = TaggableManager(verbose_name="tags", help_text=_("used to tag the posts for search optimizations, filtering, ..."))
    class Meta:
        db_table = 'posts'
        ordering = ['created_at']


    @property
    def pages(self):
        return self.medias.count()

class Like(models.Model):
    id = models.UUIDField(default = uuid4, null=False, primary_key=True, editable = False, unique=True)
    user = models.ForeignKey(Account, on_delete=models.CASCADE)
    post = models.ForeignKey(Post, on_delete=models.CASCADE, related_name='posts')
    liked_at = models.DateField(auto_now_add=True)

    class Meta:
        unique_together = ["user", "post"]
        db_table = 'likes'
        ordering = ['liked_at']


class Comment(models.Model):
    id = models.UUIDField(default = uuid4, null=False, primary_key=True, editable = False, unique=True)
    user = models.ForeignKey(Account, on_delete=models.CASCADE)
    post = models.ForeignKey(to = Post, on_delete=models.CASCADE, related_name="post_comments")
    content = models.CharField(max_length=300)
    likes_count = models.PositiveBigIntegerField(default = 0)
    commented_at = models.DateField(auto_now_add=True)    

    class Meta:
        db_table = 'comments'

class MediaPost(models.Model):
    id = models.UUIDField(default = uuid4, null=False, primary_key=True, editable = False, unique=True)
    post_id = models.ForeignKey(Post, on_delete=models.CASCADE, related_name="medias")
    content_url = models.ImageField(max_length=200, upload_to=settings.DEFAULT_POST_DIR)
    posted_at = models.DateField(auto_now_add=True)
    page_num = models.IntegerField(null=False, default=1)

    class Meta:
        unique_together = ('post_id', 'page_num')
        ordering = ['posted_at']
        db_table = "media_post"
