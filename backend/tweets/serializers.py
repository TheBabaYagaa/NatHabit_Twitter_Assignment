

from tweets.models import Tweet
from rest_framework import serializers

class TweetSerializer(serializers.ModelSerializer):
    author_username = serializers.CharField(source='author.username', read_only=True)
    likes_count = serializers.IntegerField(source='likes.count', read_only=True)
    comments_count = serializers.IntegerField(source='comments.count', read_only=True)


    class Meta:
        model = Tweet
        fields = ['id','body','author','author_username','created_at','likes_count','comments_count']
        read_only_fields = ['id','author','created_at','likes_count','comments_count']

    def validate_body(self, v):
        if len(v) > 280:
         raise serializers.ValidationError('Tweet exceeds 280 characters')
        return v