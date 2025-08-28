# tweets/views.py
from rest_framework import generics, permissions
from django.db.models import Count, Q
from tweets.models import Tweet
from users.models import Follow
from tweets.serializers import TweetSerializer 

class TimelineView(generics.ListAPIView):
    permission_classes = [permissions.IsAuthenticated]
    serializer_class = TweetSerializer

    def get_queryset(self):
        u = self.request.user


     
        following_ids = Follow.objects.filter(follower=u).values_list("following_id", flat=True)



        return (
            Tweet.objects
                .select_related("author")
                .filter(author_id__in=following_ids)
                .annotate(
                    likes_count=Count("likes", distinct=True),
                    comments_count=Count("comments", distinct=True),
                )
                .order_by("-created_at")
        )
