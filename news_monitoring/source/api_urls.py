from django.urls import include, path

from rest_framework.routers import DefaultRouter

from news_monitoring.source import api_views

app_name = "source"

router = DefaultRouter()
router.register('', api_views.SourceViewSet, basename='source')

urlpatterns = [
    path('sources/', api_views.index, name="index"),

    path('', include(router.urls)),
]
