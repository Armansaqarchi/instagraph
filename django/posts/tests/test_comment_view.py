from rest_framework.test import APITestCase
from django.contrib.auth.models import User
from ..models import Post, Comment
from accounts.models import Follows


class CommentTestCase(APITestCase):

    def setUp(self) -> None:
        self.user1 = User.objects.create_user(
            username = "Arman",
            password = "Armans8118"
        )
        self.user2 = User.objects.create_user(
            username = "Arman2",
            password = "Armans8118"
        )
        self.user3 = User.objects.create_user(
            username = "Arman3",
            password = "Armans8118"
        )
        self.follow1 = Follows.objects.create(
            follower = self.user2.account,
            following = self.user1.account
        )
        self.user1.account.is_private = True
        self.user1.account.save()
        self.post1 = Post.objects.create(
            user = self.user1.account,
            description = "some fake description",
            location = "bruh abad"
        )
        self.comment1 = Comment.objects.create(
            user = self.user2.account,
            content = "test",
            post = self.post1
        )
    

    def test_comment_create_owner(self):
        login = self.client.login(username = "Arman", password = "Armans8118")
        self.assertTrue(login)
        comment_data = {
            "content" : "test",
        }
        res = self.client.post(f"/posts/comments/create/{self.post1.id}", comment_data)
        self.assertEqual(res.status_code, 201)


    def test_comment_create_follower(self):
        login = self.client.login(username = "Arman2", password = "Armans8118")
        self.assertTrue(login)
        comment_data = {
            "content" : "test",
        }
        res = self.client.post(f"/posts/comments/create/{self.post1.id}", comment_data)
        self.assertEqual(res.status_code, 201)


    def test_comment_create_no_permission(self):
        login = self.client.login(username = "Arman3", password = "Armans8118")
        self.assertTrue(login)
        comment_data = {
            "content" : "test",
        }
        res = self.client.post(f"/posts/comments/create/{self.post1.id}", comment_data)
        self.assertEqual(res.status_code, 403)

    def test_comment_delete_success(self):
        login = self.client.login(username = "Arman2", password = "Armans8118")
        self.assertTrue(login)
        res = self.client.delete(f"/posts/comments/delete/{self.comment1.id}")
        print(res.content)
        self.assertEqual(res.status_code, 204)

    def test_comment_delete_no_permission(self):
        login = self.client.login(username = "Arman", password = "Armans8118")
        self.assertTrue(login)
        res = self.client.delete(f"/posts/comments/delete/{self.comment1.id}")
        print(res.content)
        self.assertEqual(res.status_code, 403)

    

    