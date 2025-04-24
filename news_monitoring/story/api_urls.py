from django.urls import include, path
from rest_framework.decorators import api_view
from rest_framework.routers import DefaultRouter

from news_monitoring.story.api_views import StoryViewSet, angular_index

app_name = "story"

router = DefaultRouter()
router.register('', StoryViewSet, basename='story')

urlpatterns = [
    path("stories/", angular_index, name="angular-index"),

    path('', include(router.urls)),
]
