from django.db import models
from tweets.models import Tweet
from django.conf import settings


User = settings.AUTH_USER_MODEL


class Like(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE, related_name='likes')
    tweet = models.ForeignKey(Tweet, on_delete=models.CASCADE, related_name='likes')
    created_at = models.DateTimeField(auto_now_add=True)


    class Meta:
        unique_together = ('user','tweet')


class Comment(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE, related_name='comments')
    tweet = models.ForeignKey(Tweet, on_delete=models.CASCADE, related_name='comments')
    comment_body = models.CharField(max_length=280)
    created_at = models.DateTimeField(auto_now_add=True)


    class Meta:
        ordering = ['created_at']