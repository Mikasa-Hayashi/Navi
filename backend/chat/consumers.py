import json
from asyncio import sleep
from .models import Conversation, Message
from channels.generic.websocket import AsyncWebsocketConsumer


class ChatConsumer(AsyncWebsocketConsumer):
    async def connect(self):
        self.conversation_id = self.scope['url_route']['kwargs']['conversation_id']
        self.group_name = f'conversation_{self.conversation_id}' 

        await self.channel_layer.group_add(
            self.group_name,
            self.channel_name,
        )

        await self.accept()

        await self.send(text_data=json.dumps({
            'type': 'connection_established',
            'message': 'Hello, my creator! You are connected now!',
        }))
    

    async def disconnect(self, close_code):
        await self.channel_layer.group_discard(
            self.group_name,
            self.channel_name,
        )


    async def receive(self, text_data):
        text_data_json = json.loads(text_data)
        message = text_data_json['message']
        await self.save_message(message, 'user')

        await self.send(text_data=json.dumps({
                'type': 'message',
                'message': message,
            }))
        
        await self.channel_layer.group_send(self.group_name, {
            'consumer': self.channel_name,
            'type': 'chat_message',
            'message': message,
        })

        await sleep(2)

        companion_message = f'I will be able to answer to this soon: {message}'
        await self.save_message(companion_message, 'companion')
        await self.channel_layer.group_send(self.group_name, {
            'consumer': 'other_consumer',
            'type': 'chat_message',
            'message': companion_message,
        })


    async def chat_message(self, event):
        if event['consumer'] != self.channel_name:
            await self.send(text_data=json.dumps({
                'type': 'message',
                'message': event['message'],
            }))


    async def save_message(self, content, sender_type):
        try:
            conversation = await Conversation.objects.aget(id=self.conversation_id)
            await Message.objects.acreate(
                content=content,
                sender_type=sender_type,
                conversation_id=conversation,
            )
        except Exception as e:
            print(f'Can not save message to database: {e}')
