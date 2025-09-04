from rest_framework import serializers
from .models import Conversation, Message

class ConversationSerializer(serializers.ModelSerializer):
    class Meta:
        model = Conversation
        fields = '__all__'


class MessageSerializer(serializers.ModelSerializer):
    class Meta:
        model = Message
        fields = ['id', 'content', 'created_at', 'sender_type']
        # exclude = ['conversation_id']