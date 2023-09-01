from django.test import TestCase
from channels.testing import WebsocketCommunicator, ChannelsLiveServerTestCase
from .consumers import ChatConsumer
from django.contrib.auth.models import User
from instagraph.asgi import application
from .models.chatModel import PrivateChat, GroupChat
from accounts.models import Account
from asgiref.sync import sync_to_async

class TestChat(ChannelsLiveServerTestCase):


    def setUp(self) -> None:
        self.user1 = User.objects.create_user(
            username="Arman",
            password="Armans8118"
        )
        self.user2 = User.objects.create_user(
            username= "Arman2",
            password= "Armans8118"
        )
        self.private_chat1 = PrivateChat.objects.create(
            member1 = self.user1.account,
            member2 = self.user2.account
        )
        res = self.client.post("/api/token", data={"username" : "Arman", "password": "Armans8118"})
        self.valid_access1 = res.json()["access"]
        res = self.client.post("/api/token", data={"username" : "Arman2", "password": "Armans8118"})
        self.valid_access2 = res.json()["access"]

        self.client.login(username = "Arman", password = "Armans8118")
        

    async def test_connect_consumer(self):

        communicator = WebsocketCommunicator(
            application,
            f"chat/?thread={self.private_chat1.thread.thread}",  # Adjust the URL to match your routing configuration
            headers={"Authorization": f"Bearer {self.valid_access1}"},
        )

        connected, _ = await communicator.connect()
        self.assertTrue(connected)

    async def test_send_consumer(self):
        communicator1 = WebsocketCommunicator(
            application,
            f"chat/?thread={self.private_chat1.thread.thread}",  # Adjust the URL to match your routing configuration
            headers={"Authorization": f"Bearer {self.valid_access1}"},
        )

        communicator2 = WebsocketCommunicator(
            application,
            f"chat/?thread={self.private_chat1.thread.thread}",  # Adjust the URL to match your routing configuration
            headers={"Authorization": f"Bearer {self.valid_access2}"},
        )

        await communicator1.connect()
        await communicator2.connect()

        # Test sending text
        await communicator1.send_to(text_data="hello1")
        res1 = await communicator1.receive_output()
        await communicator2.send_to(text_data="hello2")
        res2 = await communicator2.receive_output()

        self.assertEqual(res1["type"], "websocket.send")
        self.assertEqual(res2["type"], "websocket.send")

        # now we have two messages sent, lets try retreiving them using http request
        
        res = await sync_to_async(self.client.get)(
            f"/chats/chats/{self.private_chat1.thread.thread}?page=0"
        )
        
    
    def test_get_chat_lists(self):
        response = self.client.get("/chats/list")
        print(response.content)
        self.assertEqual(response.status_code, 200)

        
        

class TestUtilities(TestCase):
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
        self.chat1 = PrivateChat.objects.create(
            member1 = self.user1.account,
            member2 = self.user2.account
        )
        self.chat2 = PrivateChat.objects.create(
            member1 = self.user3.account,
            member2 = self.user1.account
        )
        self.group1 = GroupChat.objects.create(
            
        )
        self.client.login(username = "Arman", password = "Armans8118")

    def test_account_chats(self):
        chat_list = self.user1.account.chats
        self.assertEqual(len(chat_list), 2)
        print(chat_list)
        


