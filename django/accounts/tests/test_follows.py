from rest_framework.test import APITestCase
from django.contrib.auth.models import User
from ..models import FollowRQ
from ..models import Follows


class FollowerTestCase(APITestCase):
    def setUp(self) -> None:
        self.user1 = User.objects.create_user(
            username = "Arman1",
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
        self.user4 = User.objects.create_user(
            username = "Arman4",
            password = "Armans8118"
        )
        self.fr1_2 = FollowRQ.objects.create(
            sender = self.user1.account,
            recipient = self.user2.account
        )
        self.fr3_2 = Follows.objects.create(
            follower = self.user3.account,
            following = self.user2.account
        )

    def test_add_follower(self):
        self.client.login(username = "Arman2", password = "Armans8118")
        res = self.client.get(f"/accounts/follower/{self.fr1_2.id}")
        self.assertEqual(res.status_code, 200)
        self.assertEqual(res.json()["Code"],"following_accepted")


    def test_reject_follower(self):
        self.client.login(username = "Arman", password = "Armans8118")
        res = self.client.get(f"/accounts/follower/{self.fr1_2.id}?accepted=False")
        self.assertEqual(res.status_code, 200)
        self.assertEqual(res.json()["Code"],"following_rejected")
        
    def test_list_follower(self):
        self.client.login(username = "Arman2", password = "Armans8118")
        self.client.get(f"/accounts/follower/followers")

    def test_list_following(self):
        self.client.login(username = "Arman3", password = "Armans8118")
        res = self.client.get("/accounts/following/followings")
        self.assertEqual(res.status_code, 200)
        self.assertEqual(len(res.json()["Followings"]), 1)
    def test_delete_follower(self):
        f2_3 = Follows.objects.create(
            follower = self.user2.account,
            following = self.user3.account
        )
        f2_3 = Follows.objects.create(
            follower = self.user4.account,
            following = self.user3.account
        )
        login = self.client.login(username = "Arman3", password = "Armans8118")
        self.assertTrue(login)
        res = self.client.delete(f"/accounts/follower/{f2_3.id}")
        self.assertEqual(res.status_code, 204)
        followers = self.user3.account.followers_list
        self.assertEqual(len(followers), 1)

    def test_delete_follower_fail(self):
        f2_3 = Follows.objects.create(
            follower = self.user2.account,
            following = self.user3.account
        )
        f2_3 = Follows.objects.create(
            follower = self.user4.account,
            following = self.user3.account
        )
        some_wrong_id = "1234-test-1234"
        login = self.client.login(username = "Arman3", password = "Armans8118")
        res = self.client.delete(f"/accounts/follower/{some_wrong_id}")
        self.assertEqual(res.status_code, 404)

    def test_add_follower_fail(self):
        self.client.login(username = "Arman2", password = "Armans8118")
        some_wrong_fr_id = "wrong-1234"
        res = self.client.get(f"/accounts/follower/{some_wrong_fr_id}")
        self.assertEqual(res.status_code, 404)
        self.assertEqual(res.json()["Code"],"fr_not_found")


class FollowingTestCase(APITestCase):

    def setUp(self) -> None:
        self.user1 = User.objects.create_user(
            username = "Arman1",
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

    def test_add_following(self):
        login = self.client.login(username = "Arman1", password = "Armans8118")
        self.assertTrue(login)
        res = self.client.get(f"/accounts/following/{self.user2.account.id}")
        self.assertEqual(res.status_code, 200)
        followings = Follows.objects.filter(follower = self.user1.account)
        self.assertEqual(len(followings), 1)

    def test_delete_following(self):
        login = self.client.login(username = "Arman1", password = "Armans8118")
        f1_2 = Follows.objects.create(
            follower = self.user1.account,
            following = self.user2.account
        )
        self.assertTrue(login)

        followings_before = Follows.objects.filter(follower = self.user1.account, following = self.user2.account)
        self.assertEqual(len(followings_before), 1)

        res = self.client.delete(f"/accounts/following/{f1_2.id}")
        self.assertEqual(res.status_code, 204)
        followings_after = Follows.objects.filter(follower = self.user1.account, following = self.user2.account)
        self.assertEqual(len(followings_after), 0)


    def test_add_following_fail(self):
        login = self.client.login(username = "Arman1", password = "Armans8118")
        some_random_id = 4213
        res = self.client.get(f"/accounts/following/{some_random_id}")
        self.assertEqual(res.status_code, 404)

    def test_delete_following_fail(self):
        login = self.client.login(username = "Arman1", password = "Armans8118")
        some_random_id = 4213
        res = self.client.delete(f"/accounts/following/{some_random_id}")
        self.assertEqual(res.status_code, 404)
    
    
class FollowRequestTestCase(APITestCase):
    def setUp(self) -> None:
        self.users = []
        for i in range (10):
            self.users.append(User.objects.create_user(
                username = f"Arman{i}",
                password = "Armans8118"
            ))
        FollowRQ.objects.bulk_create(
            [FollowRQ(
                sender = self.users[i].account,
                recipient = self.users[9].account
            ) for i in range(9)]
        )
    def test_request_list(self):
        login = self.client.login(username = "Arman9", password = "Armans8118")
        self.assertTrue(login)
        res = self.client.get("/accounts/follower/requests")
        self.assertEqual(res.status_code, 200)
        
