from rest_framework.test import APITestCase
from django.contrib.auth.models import User
from ..models import Post, Comment


class CommentTestCase(APITestCase):

    def setUp(self) -> None:
        self.user1 = User.objects.create(
            username = "Arman",
            password = "Armans8118"
        )
        self.post1 = Post.objects.create(
            username = "Arman2",
            password = "Armans8118"
        )
        # self.comment1 = Comment.objects.create(
        #     user = self.user1
        #     content = "test",
        #     post = self.post1
        # )
    

    def test_comment_create(self):
        login = self.client.login(username = "Arman", password = "Armans8118")
        self.assertTrue(login)
        self.clinet.get("")
    

    def test_comment_delete(self):
        pass

    def test_comment_delete_no_permissions(self):
        pass

    