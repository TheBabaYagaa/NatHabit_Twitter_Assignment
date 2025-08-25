from rest_framework import permissions, status
from rest_framework.response import Response
from rest_framework.views import APIView
from .models import Like, Comment
from .serializers import LikeSerializer, CommentSerializer
from tweets.models import Tweet
from rest_framework import generics


class LikeToggleView(APIView):
    permission_classes = [permissions.IsAuthenticated]


    def post(self, request, id):
        tweet = generics.get_object_or_404(Tweet, id=id)
        like, created = Like.objects.get_or_create(user=request.user, tweet=tweet)
        if not created:
            like.delete()
            return Response({'Unliked': True})
        return Response({'liked': True})


class CommentCreateView(generics.ListCreateAPIView):
    serializer_class = CommentSerializer
    permission_classes = [permissions.IsAuthenticated]
    queryset = Comment.objects.all()


    def perform_create(self, serializer):
        tweet_id = self.kwargs['id']
        tweet = generics.get_object_or_404(Tweet, id=tweet_id)
        serializer.save(user=self.request.user, tweet=tweet)

