from django.db import models
from django.conf import settings
from django.contrib.auth.models import AbstractUser

class User(AbstractUser):
    email = models.EmailField(unique=True)
    # following = models.ManyToManyField("self", symmetrical=False, related_name="followers", blank=True)
    # # REQUIRED_FIELDS = ['email']


User = settings.AUTH_USER_MODEL

class Follow(models.Model):
    follower = models.ForeignKey(User, on_delete=models.CASCADE, related_name='following')
    following = models.ForeignKey(User, on_delete=models.CASCADE, related_name='followers')
    created_at = models.DateTimeField(auto_now_add=True)


    class Meta:
        unique_together = ('follower','following')
        indexes = [
        models.Index(fields=['follower','following']),
        ]


    def __str__(self):
        return f"{self.follower} → {self.following}"