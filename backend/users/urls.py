from django.urls import path
from .views import (SignupView, LoginView, LogoutView, UserListView, UserDetailView, FollowView)

urlpatterns  = [

    path("auth/signup/", SignupView.as_view(), name="signup"),
    path("auth/login/", LoginView.as_view(), name="login"),
    path("auth/logout/", LogoutView.as_view(), name="logout"),
    path("users/", UserListView.as_view(), name="user-list"),
    path("users/<int:id>/", UserDetailView.as_view(), name="users-detail"),
    path('users/<int:id>/follow/', FollowView.as_view(), name = "follow-view"),
]