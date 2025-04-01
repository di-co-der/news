from django.urls import path

from ..source.urls import app_name
from .views import add_or_edit, delete
from .views import list

app_name = "story"
urlpatterns = [
    path("add/", add_or_edit, name="add"),
    path("list/", list, name="list"),
    path("edit/<int:story_id>/", add_or_edit, name="edit"),
    path("delete/<int:story_id>/", delete, name="delete"),
]
