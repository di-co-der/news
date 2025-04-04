from django.urls import path

from news_monitoring.source import views

app_name = "source"
urlpatterns = [
    path("", views.list_sources, name="list"),
    path("add/", views.add_or_edit_source, name="add"),
    path("edit/<int:source_id>/", views.add_or_edit_source, name="edit"),
    path("delete/<int:source_id>/", views.delete_source, name="delete"),
    path("fetch-story/<int:source_id>/", views.fetch_stories, name="fetch-story"),
    path("fetch-sources/", views.fetch_sources, name="fetch_sources"),
]
