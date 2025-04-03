from django.urls import path

from .views import add_or_edit_source, fetch_story
from .views import delete_source
from .views import list_sources

app_name = "source"
urlpatterns = [
    path("add/", add_or_edit_source, name="add"),
    path("edit/<int:source_id>/", add_or_edit_source, name="edit"),
    path("delete/<int:source_id>", delete_source, name="delete"),
    path("fetch-css/<int:source_id>/", fetch_story, name="fetch_story"),
    path("", list_sources, name="list"),
]
