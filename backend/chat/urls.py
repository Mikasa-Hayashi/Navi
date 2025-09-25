from django.urls import path
from . import views

app_name = 'conversations'

urlpatterns = [
    path('', views.ConversationListView.as_view(), name='conversation_list'),
    path('<uuid:conversation_id>/', views.ConversationDetailView.as_view(), name='conversation_detail'),
    path('<uuid:conversation_id>/messages/', views.MessageListView.as_view(), name='message_list'),
    path('<uuid:conversation_id>/messages/<int:message_id>', views.MessageDetailView.as_view(), name='message_detail'),
]