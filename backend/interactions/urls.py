from django.urls import path
from .views import LikeToggleView, CommentCreateView


urlpatterns = [
path('tweets/<int:id>/like/', LikeToggleView.as_view()),
path('tweets/<int:id>/comments/', CommentCreateView.as_view()),
# path('tweets/<int:id>/comments/', CommentCreateView.as_view()), #POST

]