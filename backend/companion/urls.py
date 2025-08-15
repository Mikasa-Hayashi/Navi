from django.urls import path
from . import views

app_name = 'companion'

urlpatterns = [
    path('create/', views.create_companion, name='create'),
]