from django.urls import path
from .views import TweetListCreateView, TweetDetailView


urlpatterns = [
path('tweets/', TweetListCreateView.as_view()),
path('tweets/<int:id>/', TweetDetailView.as_view()),
]