from django.contrib.auth.decorators import login_required
from django.shortcuts import render, redirect
from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import status
from .models import Conversation, Message
from .serializers import ConversationSerializer, MessageSerializer
from companion.models import Companion

# Create your views here.
class ConversationListView(APIView):
    def get(self, request):
        conversations = Conversation.objects.filter(user_id=request.user)
        serializer = ConversationSerializer(conversations, many=True)
        return Response(serializer.data)

    def post(self, request):
        companion_id = request.data.get('companion_id')
        if not companion_id:
            return Response({'detail': 'companion_id is required'}, status=status.HTTP_400_BAD_REQUEST)

        try:
            companion = Companion.objects.get(id=companion_id, owner_id=request.user)
        except Companion.DoesNotExist:
            return Response({'detail': 'Companion not found'}, status=status.HTTP_404_NOT_FOUND)

        if Conversation.objects.filter(user_id=request.user, companion_id=companion).exists():
            return Response(
                {'detail': 'Chat with this companion already exists'},
                status=status.HTTP_409_CONFLICT
            )

        if Conversation.objects.filter(user_id=request.user).count() >= 2:
            return Response(
                {'detail': 'Maximum number of chats reached'},
                status=status.HTTP_409_CONFLICT
            )

        conversation = Conversation.objects.create(
            title=companion.name,
            user_id=request.user,
            companion_id=companion,
        )
        serializer = ConversationSerializer(conversation)
        return Response(serializer.data, status=status.HTTP_201_CREATED)

class ConversationDetailView(APIView):
    def get(self, request, *args, **kwargs):
        conversation_id = kwargs.get('conversation_id')
        conversation = Conversation.objects.get(id=conversation_id, user_id=request.user)
        serializer = ConversationSerializer(conversation)
        return Response(serializer.data)

    def delete(self, request, *args, **kwargs):
        conversation_id = kwargs.get('conversation_id')
        try:
            conversation = Conversation.objects.get(id=conversation_id, user_id=request.user)
        except Conversation.DoesNotExist:
            return Response({'detail': 'Conversation not found'}, status=status.HTTP_404_NOT_FOUND)

        conversation.delete()
        return Response(status=status.HTTP_204_NO_CONTENT)

class MessageListView(APIView):
    def get(self, request, *args, **kwargs):
        conversation_id = kwargs.get('conversation_id')
        messages = Message.objects.filter(conversation_id=conversation_id, conversation_id__user_id=request.user)
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