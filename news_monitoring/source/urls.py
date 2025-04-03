from django.urls import path

from ..users.urls import app_name
from .views import add_or_edit_source
from .views import delete_source
from .views import list_sources

app_name = "source"
urlpatterns = [
    path("add/", add_or_edit_source, name="add"),
    path("edit/<int:source_id>/", add_or_edit_source, name="edit"),
    path("delete/<int:source_id>", delete_source, name="delete"),
    path("", list_sources, name="list"),
]
