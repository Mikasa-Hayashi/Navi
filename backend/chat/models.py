from django.db import models
from django.contrib.auth.models import User

# Create your models here.
class Conversation(models.Model):
    id = models.UUIDField(primary_key=True)
    title = models.CharField(max_length=75)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    user_id = models.ForeignKey(User, on_delete=models.CASCADE)
    companion_id = models.ForeignKey('companion.Companion', on_delete=models.CASCADE)

    def __str__(self):
        return self.title
    
    class Meta:
        ordering = ['updated_at']


class Message(models.Model):
    content = models.TextField()
    created_at = models.DateTimeField()
    sender_type = models.CharField(max_length=10, choices=[('user', 'User'), ('companion', 'Companion')])
    conversation_id = models.ForeignKey(Conversation, on_delete=models.CASCADE)

    def __str__(self):
        return f'Message: {self.content}'
    
    class Meta:
        ordering = ['created_at']