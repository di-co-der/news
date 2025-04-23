from django.urls import include, path

from rest_framework.routers import DefaultRouter

from news_monitoring.source.api_views import SourceViewSet, angular_index

app_name = "source"

router = DefaultRouter()
router.register(r'sources', SourceViewSet, basename='source')

urlpatterns = [
    path('', include(router.urls)),
    path('api-auth/', include('rest_framework.urls', namespace='rest_framework')),

    path("source-angular/", angular_index, name="angular-index"),
    path('source-angular/<path:path>', angular_index, name="angular-catch-all"),
]


# Method	Endpoint	Description
# GET	/sources/	List sources
# POST	/sources/	Create source
# GET	/sources/{id}/	Get source detail
# PUT	/sources/{id}/	Full update
# PATCH	/sources/{id}/	Partial update
# DELETE	/sources/{id}/	Delete source
# GET	/sources/{id}/fetch-stories/	Fetch stories for the source
# GET	/sources/search/?q=...	Search sources (with pagination)
# GET	/sources/form-data/?source_id=...	Get form data for add/edit page
