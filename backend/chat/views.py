from django.contrib.auth.decorators import login_required
from django.shortcuts import render, redirect
from rest_framework.views import APIView
from rest_framework.response import Response
from .models import Conversation, Message
from .serializers import ConversationSerializer, MessageSerializer

# Create your views here.
class ConversationListView(APIView):
    def get(self, request):
        conversations = Conversation.objects.filter(user_id=request.user)
        serializer = ConversationSerializer(conversations, many=True)
        return Response(serializer.data)

class ConversationDetailView(APIView):
    def get(self, request, *args, **kwargs):
        conversation_id = kwargs.get('conversation_id')
        conversation = Conversation.objects.get(id=conversation_id)
        serializer = ConversationSerializer(conversation)
        return Response(serializer.data)

class MessageListView(APIView):
    def get(self, request, *args, **kwargs):
        conversation_id = kwargs.get('conversation_id')
        messages = Message.objects.filter(conversation_id=conversation_id)
        serializer = MessageSerializer(messages, many=True)
        return Response(serializer.data)
    
class MessageDetailView(APIView):
    def get(self, request, *args, **kwargs):
        conversation_id = kwargs.get('conversation_id')
        message_id = kwargs.get('message_id')
        conversation = Conversation.objects.get(id=conversation_id)
        message = conversation.messages.get(id=message_id)
        serializer = MessageSerializer(message)
        return Response(serializer.data)
        


@login_required
def conversation_list(request):
    conversations = Conversation.objects.filter(user_id=request.user)
    return render(request, 'chat/conversation_list.html', { 'conversations': conversations })

@login_required
def conversation_detail(request, conversation_id):
    conversation = Conversation.objects.get(id=conversation_id)
    messages = conversation.messages.all()
    return render(request, 'chat/conversation_detail.html', { 
        'conversation': conversation,
        'messages': messages,
    })

def send_message(request, conversation_id):
    if request.method == 'POST':
        content = request.POST.get('text')
        if content.strip():
            conversation = Conversation.objects.get(id=conversation_id)
            Message.objects.create(
                content=content,
                sender_type='user',
                conversation_id=conversation,
            )
    return redirect('chat:conversation_detail', conversation_id=conversation_id)