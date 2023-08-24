from channels.generic.websocket import AsyncWebsocketConsumer
import json


class ChatConsumer(AsyncWebsocketConsumer):
    async def connect(self):
        # header = self.scope.get("headers")
        # if not hasattr(header, "chat_room"):
        #     await self.close()
        # chat_room = header["chat_room"]
        # self.channel_layer.
        # if self.scope.get("user").is_authenticated:
        #     await self.accept()
        pass


    async def disconnect(self, close_code):
        # Perform any necessary cleanup when a connection is closed
        pass

    async def receive(self, text_data):
        # Handle incoming messages from the client
        print("dsfagsags", self.scope)
        await self.send(text_data=text_data)
