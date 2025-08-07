import uuid
from django.db import models
from django.conf import settings

# Create your models here.
class Conversation(models.Model):
    id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)
    title = models.CharField(max_length=75, blank=False)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    user_id = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE)
    companion_id = models.ForeignKey('companion.Companion', on_delete=models.CASCADE)

    def __str__(self):
        return self.title
    
    class Meta:
        ordering = ['-updated_at'] # From new to old


class Message(models.Model):
    content = models.TextField(blank=False)
    created_at = models.DateTimeField()
    sender_type = models.CharField(max_length=10, choices=[('user', 'User'), ('companion', 'Companion')])
    conversation_id = models.ForeignKey(Conversation, on_delete=models.CASCADE, related_name='messages')

    def __str__(self):
        return f'Message: {self.content}'
    
    class Meta:
        ordering = ['created_at']