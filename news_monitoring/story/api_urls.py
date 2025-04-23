from django.urls import include, path
from rest_framework.decorators import api_view
from rest_framework.routers import DefaultRouter

from news_monitoring.story.api_views import StoryViewSet, angular_index

app_name = "story"

router = DefaultRouter()
router.register(r'stories', StoryViewSet, basename='story')

urlpatterns = [
    path('', include(router.urls)),
    path('api-auth/', include('rest_framework.urls', namespace='rest_framework')),

    # Angular App Shell (renders index.html)

    path("story-angular/", angular_index, name="angular-index"),
    path('story-angular/<path:path>', angular_index, name="angular-catch-all"),
]
