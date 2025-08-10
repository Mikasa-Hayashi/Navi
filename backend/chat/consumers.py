import json
from channels.generic.websocket import AsyncWebsocketConsumer
from asyncio import sleep

class ChatConsumer(AsyncWebsocketConsumer):
    async def connect(self):
        await self.accept()

        await self.send(text_data=json.dumps({
            'type': 'connection_established',
            'message': 'Hello, my creator! You are connected now!'
        }))
    
    async def receive(self, text_data):
        text_data_json = json.loads(text_data)
        message = text_data_json['message']

        for i in range(20):
            await self.send(text_data=json.dumps({
                'type': 'message',
                'message': f'message #{i}'
            }))
            await sleep(0.5)
