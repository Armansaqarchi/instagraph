from rest_framework.test import APITestCase
from ..models import Post
from django.contrib.auth.models import User
from ..models import Like
from ..serializer.Homeserializer import LikesSerializer


class TestLikeSerializer(APITestCase):

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

    
    def test_like_serializer(self):
        like = LikesSerializer(instance= [self.like1, self.like2], many = True, context = {"account" : self.user1.account})
        self.assertEqual(len(like.data), 2)