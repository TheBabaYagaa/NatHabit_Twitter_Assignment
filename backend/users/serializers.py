from django.contrib.auth import get_user_model
from django.contrib.auth.password_validation import validate_password
from rest_framework import serializers
from django.db import transaction
from .models import Follow

User = get_user_model()

class UserSerializer(serializers.ModelSerializer):
    class Meta:
        model = User
        fields = ["id", "username", "email"]


class UserDetailSerializer(serializers.ModelSerializer):
    followers_count = serializers.SerializerMethodField()
    following_count = serializers.SerializerMethodField()
    followers = serializers.SerializerMethodField()
    following = serializers.SerializerMethodField()

    class Meta:
        model = User
        fields = [
            "id", "username", "email",
            "followers_count", "following_count",
            "followers", "following",
        ]

    def get_followers_count(self, obj):
        return Follow.objects.filter(following=obj).count()

    def get_following_count(self, obj):
        return Follow.objects.filter(follower=obj).count()

    def get_followers(self, obj):
        ids = Follow.objects.filter(following=obj).values_list("follower_id", flat=True)
        users = User.objects.filter(id__in=ids).order_by("id").distinct()
        return UserSerializer(users, many=True).data

    def get_following(self, obj):
        ids = Follow.objects.filter(follower=obj).values_list("following_id", flat=True)
        users = User.objects.filter(id__in=ids).order_by("id").distinct()
        return UserSerializer(users, many=True).data



class SignupSerializer(serializers.ModelSerializer):
    password = serializers.CharField(write_only=True, min_length=6)
    confirm_password = serializers.CharField(write_only=True, min_length=6)
    class Meta:
        model = User
        fields = ["username", "email", "password","confirm_password"]

    def validate_email(self, value):
        if User.objects.filter(email=value).exists():
            raise serializers.ValidationError("A user with this email already exists.")
        return value

    def validate(self, data):
        if data["password"] != data["confirm_password"]:
            raise serializers.ValidationError("Password does not match")
        validate_password(data["password"]); return data
    
    @transaction.atomic
    def create(self, data):
        data.pop("confirm_password")
        user = User.objects.create_user(
            username=data["username"], email=data.get("email",""), password=data["password"]
        )
        return user


class FollowSerializer(serializers.ModelSerializer):
    class Meta:
        model = Follow
        fields = ['id','follower','following','created_at']
        read_only_fields = ['id','created_at','follower']