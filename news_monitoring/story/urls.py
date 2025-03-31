from django.urls import path

from ..source.urls import app_name
from .views import add_story
from .views import list_stories

app_name = "story"
urlpatterns = [
    path("add/", add_story, name="add"),
    path("list/", list_stories, name="list_stories"),
]
