from django.db import models
from django.conf import settings

# Create your models here.
class Companion(models.Model):
    name = models.CharField(max_length=255, blank=False)
    birth_date = models.DateTimeField()
    gender = models.CharField(max_length=7, blank=False, choices=[('male', 'Male'), ('female', 'Female')])
    eye_color = models.CharField(max_length=50, blank=False)
    hair_color = models.CharField(max_length=50, blank=False)
    avatar = models.URLField()
    created_at = models.DateTimeField(auto_now_add=True)
    owner_id = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE)

    def __str__(self):
        return self.name
    
    class Meta:
        ordering = ['created_at']