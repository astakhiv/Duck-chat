import json
import os
import django
os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'rest.settings')
os.environ["DJANGO_ALLOW_ASYNC_UNSAFE"] = "true"
django.setup()

from channels.generic.websocket import AsyncWebsocketConsumer
from .models import Chat, Message, User

class ChatConsumer(AsyncWebsocketConsumer):
    async def connect(self):
        self.roomGroupName = 'group'
        await self.channel_layer.group_add(
            self.roomGroupName,
            self.channel_name
        )
        await self.accept()

    async def disconnect(self, close_code):
        await self.channel_layer.group_discard(
            self.roomGroupName,
            self.channel_layer
        )

    async def receive(self, text_data):
        text_data_json = json.loads(text_data)
        message = text_data_json.get("message")
        message_sender = text_data_json.get("from")
        message_receiver = text_data_json.get("to")
        print(message_sender)

        sender = User.objects.get(username=message_sender)
        receiver = User.objects.get(username=message_receiver)
        chat = Chat.objects.filter(participants__in=[sender, receiver])[0]

        new_message = Message(sender=sender, message=message, chat=chat)

        new_message.save()

        await self.channel_layer.group_send(
            self.roomGroupName, {
                "type": "sendMessage",
                "message": message,
                "username": message_sender,
                "added to base": "success",
            }
        )
    
    async def sendMessage(self, event):
        message = event["message"]
        username = event["username"]
        await self.send(text_data= json.dumps({
            "message":message, 
            "username": username
            })
        )