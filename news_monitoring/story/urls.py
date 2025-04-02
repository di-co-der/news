from django.urls import path

from ..source.urls import app_name
from .views import add_or_edit, delete, autocomplete_stories, search_stories
from .views import list

app_name = "story"
urlpatterns = [
    path("add/", add_or_edit, name="add"),
    path("list/", list, name="list"),
    path("edit/<int:story_id>/", add_or_edit, name="edit"),
    path("delete/<int:story_id>/", delete, name="delete"),
    path('search/', search_stories, name='search'),
    path('autocomplete/', autocomplete_stories, name='autocomplete'),
]
