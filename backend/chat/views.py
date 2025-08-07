from django.shortcuts import render
from .models import Conversation

# Create your views here.
def conversation_list(request):
    conversations = Conversation.objects.all()
    return render(request, 'chat/conversation_list.html', { 'conversations': conversations })

def conversation_detail(request, uuid):
    conversation = Conversation.objects.get(id=uuid)
    return render(request, 'chat/conversation_detail.html', { 'conversation': conversation })