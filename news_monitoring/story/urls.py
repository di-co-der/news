from django.urls import path

from .views import add_or_edit, delete, list_stories

app_name = "story"
urlpatterns = [
    path("add/", add_or_edit, name="add"),
    path("list/", list_stories, name="list"),
    path("edit/<int:story_id>/", add_or_edit, name="edit"),
    path("delete/<int:story_id>/", delete, name="delete"),
    # path('search/', list_stories, name='search'),
    # path('autocomplete/', autocomplete_stories, name='autocomplete'),
]
