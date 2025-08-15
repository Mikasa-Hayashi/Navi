from django.shortcuts import render, redirect
from .forms import CompanionCreationForm
from chat.models import Conversation

# Create your views here.
def create_companion(request):
    if request.method == 'POST':
        form = CompanionCreationForm(request.POST)
        if form.is_valid():
            companion = form.save(commit=False)
            companion.owner_id = request.user
            companion.save()
            if form.cleaned_data['create_conversation']:
                conversation = Conversation.objects.create(
                    title=companion.name,
                    user_id=request.user,
                    companion_id=companion,
                )
                return redirect('chat:conversation_detail', conversation_id=conversation.id)
            else:
                return redirect('chat:conversation_list')
    else:
        form = CompanionCreationForm()
    return render(request, 'companion/create.html', { 'form': form })