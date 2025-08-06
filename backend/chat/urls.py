from django.urls import path
from . import views

urlpatterns = [
    path('', views.conversation_list, name='conversations'),
    path('<uuid:uuid>', views.conversation_detail, name='conversation'),
]