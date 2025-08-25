from rest_framework import serializers
from .models import Like, Comment
from tweets.serializers import TweetSerializer 


class LikeSerializer(serializers.ModelSerializer):
    class Meta:
        model = Like
        fields = ['id','user','tweet','created_at']
        read_only_fields = ['id','user','created_at']


class CommentSerializer(serializers.ModelSerializer):
    user_username = serializers.CharField(source='user.username', read_only=True)
    tweet_id = serializers.PrimaryKeyRelatedField(read_only=True)
    tweet_detail = TweetSerializer(source='tweet', read_only=True)
    


    class Meta:
        model = Comment
        fields = ['id','user_username','tweet_id','tweet_detail','comment_body','created_at']
        read_only_fields = ['id','user','created_at']


    def validate_text(self, v):
        if not v.strip():
            raise serializers.ValidationError('Empty comment')
        if len(v) > 280:
            raise serializers.ValidationError('Comment exceeds 280 characters')
        return v