from django.shortcuts import render, redirect
from .models import Conversation, Message

# Create your views here.
def conversation_list(request):
    conversations = Conversation.objects.all()
    return render(request, 'chat/conversation_list.html', { 'conversations': conversations })

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