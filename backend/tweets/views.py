from django.shortcuts import render
from rest_framework import permissions, generics
from .serializers import TweetSerializer
from tweets.models import Tweet
from rest_framework.response import Response
from rest_framework.views import APIView
from django.db.models import Count


class TweetListCreateView(generics.ListCreateAPIView):
    # queryset = (
    #     Tweet.objects.select_related('author')
    #     .annotate(
    #         likes_count=Count('likes', distinct=True),
    #         comments_count=Count('comments', distinct=True),
    #     )
    #     .order_by('-created_at')
    # )
    queryset = Tweet.objects.select_related('author').all()
    serializer_class = TweetSerializer
    permission_classes = [permissions.IsAuthenticated]

    def perform_create(self, serializer):
        serializer.save(author = self.request.user)

class TweetDetailView(generics.RetrieveAPIView):
    queryset = Tweet.objects.select_related('author')
    serializer_class = TweetSerializer
    permission_classes = [permissions.IsAuthenticated]
    lookup_field = 'id'



