from rest_framework.test import APITestCase
from django.contrib.auth.models import User
from .models import Follows


class AccountTestCase(APITestCase):

    def setUp(self) -> None:
        user1 = User.objects.create_user(
            username= "Arman1",
            password= "Armans8118"
        )
        user2 = User.objects.create_user(
            username= "Arman2",
            password= "Armans8118"
        )
        user3 = User.objects.create_user(
            username= "Arman3",
            password= "Armans8118"
        )
        user4 = User.objects.create_user(
            username= "Arman4",
            password= "Armans8118"
        )
        self.user5 = User.objects.create_user(
            username= "shahin",
            password= "Armans8118"
        )
        self.users_list = [user1, user2, user3, user4]
        Follows.objects.bulk_create(
            Follows(
            follower = user.account,
            following = self.user5.account
            )
            for user in self.users_list
        )
        Follows.objects.bulk_create(
            Follows(
            following = user.account,
            follower = self.user5.account
            )
            for user in self.users_list
        )
        
    def test_follower_list(self): 
        followers = self.user5.account.followers_list
        self.assertEqual(4, len(followers))
    

    def test_following_list(self):
        followings = self.user5.account.followings_list
        self.assertEqual(4, len(followings))