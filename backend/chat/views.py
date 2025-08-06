from django.shortcuts import render
from django.http import HttpResponse
from .models import Conversation

# Create your views here.
def conversation_list(request):
    conversations = Conversation.objects.all()
    return render(request, 'chat/conversation_list.html', { 'conversations': conversations })

def conversation_detail(request, uuid):
    return HttpResponse(Conversation.objects.get(id=uuid).title)