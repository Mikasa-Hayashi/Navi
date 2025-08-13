from django.contrib.auth import login
from django.contrib.auth.forms import AuthenticationForm
from django.shortcuts import render, redirect
from .forms import CustomUserCreationForm

# Create your views here.
def register_user(request):
    if request.method == 'POST':
        form = CustomUserCreationForm(request.POST)
        if form.is_valid():
            login(request, form.save())
            return redirect('chat:conversation_list')
    else:
        form = CustomUserCreationForm()
    return render(request, 'users/register.html', { 'form': form })

def log_in_user(request):
    if request.method == 'POST':
        form = AuthenticationForm(data=request.POST)
        if form.is_valid():
            login(request, form.get_user())
            return redirect('chat:conversation_list')
    else:
        form = AuthenticationForm()
    return render(request, 'users/login.html', { 'form': form })