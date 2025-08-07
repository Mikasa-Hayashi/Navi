from django.shortcuts import render, redirect
from .forms import CustomUserCreationForm

# Create your views here.
def register_user(request):
    if request.method == 'POST':
        form = CustomUserCreationForm(request.POST)
        if form.is_valid():
            form.save()
            return redirect('chat:conversation_list')
    else:
        form = CustomUserCreationForm()
    return render(request, 'users/register.html', { 'form': form })