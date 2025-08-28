from django.urls import path
from timelines.views import TimelineView


urlpatterns = [ path('timeline/', TimelineView.as_view()) ]