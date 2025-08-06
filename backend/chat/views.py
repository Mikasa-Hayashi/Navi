from django.shortcuts import render
from .models import Conversation

# Create your views here.
def show_chat(request):
    conversations = Conversation.objects.all()
    return render(request, 'chat/chat.html', { 'conversations': conversations })