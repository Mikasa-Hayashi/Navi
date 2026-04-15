from django.shortcuts import render, redirect
from .forms import CompanionCreationForm
from chat.models import Conversation
from .models import Companion
from .serializers import CompanionSerializer, CompanionPreviewSerializer
from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import status
from django.utils import timezone

# Create your views here.
class CompanionListView(APIView):
    def get(self, request):
        owner_id = request.user.id
        companions = Companion.objects.filter(owner_id=owner_id)
        serializer = CompanionPreviewSerializer(companions, many=True) #short form
        return Response(serializer.data)

    def post(self, request):
        if Companion.objects.filter(owner_id=request.user).count() >= 2:
            return Response(
                {'detail': 'Maximum number of companions reached'},
                status=status.HTTP_409_CONFLICT
            )

        name = (request.data.get('name') or '').strip()
        avatar = (request.data.get('avatar') or '').strip()

        if not name or not avatar:
            return Response(
                {'detail': 'Both name and avatar are required'},
                status=status.HTTP_400_BAD_REQUEST
            )

        companion = Companion.objects.create(
            name=name,
            avatar=avatar,
            owner_id=request.user,
            birth_date=timezone.now(),
            gender='female',
            eye_color='brown',
            hair_color='brown',
        )
        serializer = CompanionPreviewSerializer(companion)
        return Response(serializer.data, status=status.HTTP_201_CREATED)


class CompanionDetailView(APIView):
    def get(self, request, *args, **kwargs):
        companion_id = kwargs.get('companion_id')
        companion = Companion.objects.get(id=companion_id, owner_id=request.user)
        serializer = CompanionSerializer(companion)
        return Response(serializer.data)

    def delete(self, request, *args, **kwargs):
        companion_id = kwargs.get('companion_id')
        try:
            companion = Companion.objects.get(id=companion_id, owner_id=request.user)
        except Companion.DoesNotExist:
            return Response({'detail': 'Companion not found'}, status=status.HTTP_404_NOT_FOUND)

        companion.delete()
        return Response(status=status.HTTP_204_NO_CONTENT)


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