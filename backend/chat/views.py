from django.shortcuts import render

# Create your views here.
def show_chat(request):
    return render(request, 'chat/chat.html')