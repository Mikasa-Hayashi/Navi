from django.shortcuts import render, redirect
from .forms import CompanionCreationForm
from chat.models import Conversation
from .models import Companion
from .serializers import CompanionSerializer
from rest_framework.views import APIView
from rest_framework.response import Response

# Create your views here.
class CompanionDetailView(APIView):
    def get(self, request):
        companion = Conversation.objects.filter(companion_id=request.companion_id)
        serializer = CompanionSerializer(companion)
        return Response(serializer.data)


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