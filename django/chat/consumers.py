from channels.generic.websocket import AsyncWebsocketConsumer
from .exception_handler import ws_exception_handler


class ChatConsumer(AsyncWebsocketConsumer):

    def dispatch(self, message):
        try:
            return super().dispatch(message)
        except Exception as exc:
            context = self.scope
            ws_exception_handler(exc=exc, context=context)

    async def connect(self):
        chat = self.scope["chat"]
        if self.scope.get("user").is_authenticated:
            await self.accept()



    async def disconnect(self, close_code):
        # Perform any necessary cleanup when a connection is closed
        pass

    async def receive(self, text_data):
        # Handle incoming messages from the client
        print("dsfagsags", self.scope)
        await self.send(text_data=text_data)
