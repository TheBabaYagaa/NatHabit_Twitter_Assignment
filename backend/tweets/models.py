from django.conf import settings
from django.db import models


User = settings.AUTH_USER_MODEL


class Tweet(models.Model):
    author = models.ForeignKey(User, on_delete=models.CASCADE, related_name='tweets')
    body = models.CharField(max_length=280)
    created_at = models.DateTimeField(auto_now_add=True)


    class Meta:
        ordering = ['-created_at']


    def __str__(self):
        return f"{self.author}: {self.body}"
    
