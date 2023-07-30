from django.test import TestCase
from channels.testing import WebsocketCommunicator
from .consumers import ChatConsumer

# class testChat(TestCase):
#     async def test_chat_consumer(self):
#         communicator = WebsocketCommunicator(ChatConsumer.as_asgi(), "ws://localhost:8000/ws/")
#         communicator.scope["user"] = "test"

#         connected, subprotocol = await communicator.connect()
#         assert connected

#         await communicator.send_to(text_data="hello")
#         response = await communicator.receive_from()
#         assert response == "hello"
#         await communicator.disconnect()

