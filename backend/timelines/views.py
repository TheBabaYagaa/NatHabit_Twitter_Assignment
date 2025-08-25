# tweets/views.py
from rest_framework import generics, permissions
from django.db.models import Count, Q
from tweets.models import Tweet
from tweets.serializers import TweetSerializer 

class TimelineView(generics.ListAPIView):
    permission_classes = [permissions.IsAuthenticated]
    serializer_class = TweetSerializer

    def get_queryset(self):
        u = self.request.user

        include_self = self.request.query_params.get("include_self", "").lower() in {"1", "true", "yes"}

       
        following_ids = u.following.values_list("id", flat=True)

        author_filter = Q(author_id__in=following_ids)
        if include_self:
            author_filter |= Q(author_id=u.id)

        return (
            Tweet.objects
                 .select_related("author")
                 .filter(author_filter)
                 .annotate(
                     likes_count=Count("likes", distinct=True),
                     comments_count=Count("comments", distinct=True),
                 )
                 .order_by("-created_at")
        )
