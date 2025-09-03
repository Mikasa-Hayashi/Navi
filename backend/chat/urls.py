from django.urls import path
from . import views

app_name = 'chat'

urlpatterns = [
    path('', views.ConversationList.as_view(), name='conversation_list'),
    path('<uuid:conversation_id>', views.MessageList.as_view(), name='conversation_detail'),
    # path('<uuid:conversation_id>/send_message', views.send_message, name='send_message'),
]