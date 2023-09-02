from rest_framework.test import APITestCase
from ..models import Post, Like, Comment
from django.contrib.auth.models import User
from ..serializer.Homeserializer import LikesSerializer, CommentSerializer


class TestSerializers(APITestCase):

    def setUp(self) -> None:
        self.user1 = User.objects.create(
            username =  "Arman",
            password = "Armans8118"
        )
        self.user2 = User.objects.create(
            username =  "Arman2",
            password = "Armans8118"
        )
        self.post1 = Post.objects.create(
            user = self.user1.account,
            description = "testing post",
            location = "no where"
        )
        self.post2 = Post.objects.create(
            user = self.user1.account,
            description = "testing post2",
            location = "no where2"
        )
        self.like1 = Like.objects.create(
            user = self.user1.account,
            post = self.post1
        )
        self.like2 = Like.objects.create(
            user = self.user2.account,
            post = self.post2
        )
        self.comment1 = Comment.objects.create(
            user = self.user1,
            post = self.post1,
            content = "test"
        )
        self.comment2 = Comment.objects.create(
            user = self.user2,
            post = self.post1,
            content = "test2"
        )

    
    def test_like_serializer(self):
        likes = LikesSerializer(instance= [self.like1, self.like2], many = True, context = {"account" : self.user1.account})
        self.assertEqual(len(likes.data), 2)

    
    def test_comment_serializer(self):
        comments = CommentSerializer(comment = [self.comment1, self.comment2], many = True)
        print(comments)
        self.assertEqual(len(comments.data), 2)
