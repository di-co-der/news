from django import shortcuts

from rest_framework import viewsets, permissions, status
from rest_framework.response import Response
from rest_framework.decorators import action
from rest_framework import filters

from news_monitoring.source.models import Source
from news_monitoring.source.serializers import SourceSerializer
from news_monitoring.story.serializers import StorySerializer
from news_monitoring.source import services


class SourceViewSet(viewsets.ModelViewSet):
    """
    Handles listing, creating, updating, deleting sources
    and includes a custom action to fetch stories from a feed.
    """
    serializer_class = SourceSerializer
    permission_classes = [permissions.IsAuthenticated]
    filter_backends = [filters.SearchFilter]
    search_fields = ['name']

    def get_queryset(self):
        queryset = Source.objects.prefetch_related('tagged_companies')
        user = self.request.user
        if user.is_staff:
            return queryset
        return queryset.filter(company=user.company)

    def perform_create(self, serializer):
        company = serializer.validated_data.get('company')
        if not company:
            company = self.request.user.company
        serializer.save(added_by=self.request.user, company=company)

    def perform_update(self, serializer):
        company = serializer.validated_data.get('company')
        if not company:
            company = self.request.user.company
        serializer.save(updated_by=self.request.user, company=company)

    def destroy(self, request, *args, **kwargs):
        instance = self.get_object()
        self.perform_destroy(instance)
        return Response({"detail": "Source deleted successfully."}, status=status.HTTP_204_NO_CONTENT)

    @action(detail=True, methods=['get'], url_path='fetch-stories')
    def fetch_stories(self, request, pk=None):
        """
        Custom action to import stories from a feed and return the imported stories
        """
        source_obj, _ = services.get_source(request.user, pk)
        imported_stories = services.import_stories_from_feed(source_obj, request.user)
        serializer = StorySerializer(imported_stories, many=True)
        return Response({
            "detail": "Stories imported successfully.",
            "stories": serializer.data
        })

def index(request):
    return shortcuts.render(request, "source/index.html")
