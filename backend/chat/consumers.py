import json
from asgiref.sync import sync_to_async
from django.conf import settings
from .models import Conversation, Message
from channels.generic.websocket import AsyncWebsocketConsumer
from .serializers import MessageSerializer
from .llm_service import generate_companion_reply


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
        }))
    

    async def disconnect(self, close_code):
        await self.channel_layer.group_discard(
            self.group_name,
            self.channel_name,
        )


    async def receive(self, text_data):
        text_data_json = json.loads(text_data)
        message_content = text_data_json['message']
        history = await self.get_recent_history()
        message = await self.save_message(message_content, 'user')
        serializer = MessageSerializer(message)

        # serialize message to send to WebSocket
        await self.send(text_data=json.dumps({
            'type': 'message',
            'message': serializer.data,
        }))
        
        await self.channel_layer.group_send(self.group_name, {
            'consumer': self.channel_name,
            'type': 'chat_message',
            'message': serializer.data,
        })

        companion_name = await self.get_companion_name()
        companion_message = await sync_to_async(generate_companion_reply)(
            companion_name=companion_name,
            user_message=message_content,
            history=history,
        )

        message = await self.save_message(companion_message, 'companion')
        serializer = MessageSerializer(message)

        await self.channel_layer.group_send(self.group_name, {
            'consumer': 'other_consumer',
            'type': 'chat_message',
            'message': serializer.data,
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
            message = await Message.objects.acreate(
                content=content,
                sender_type=sender_type,
                conversation_id=conversation,
            )
            return message
        except Exception as e:
            print(f'Can not save message to database: {e}')

    async def get_companion_name(self):
        try:
            conversation = await Conversation.objects.select_related('companion_id').aget(id=self.conversation_id)
            return conversation.companion_id.name
        except Exception as e:
            print(f'Can not get companion name: {e}')
            return 'Companion'

    async def get_recent_history(self):
        history = []
        queryset = Message.objects.filter(
            conversation_id=self.conversation_id
        ).order_by('-created_at')[:settings.LLM_HISTORY_LIMIT]

        async for message in queryset:
            role = 'assistant' if message.sender_type == 'companion' else 'user'
            history.append({
                'role': role,
                'content': message.content,
            })

        history.reverse()
        return history
