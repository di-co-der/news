from django import shortcuts

from rest_framework import viewsets, permissions, status
from rest_framework.response import Response
from rest_framework.decorators import action
from rest_framework import filters
from rest_framework import serializers

from news_monitoring.company.models import Company
from news_monitoring.source.models import Source
from news_monitoring.source.serializers import SourceSerializer
from news_monitoring.story.serializers import StorySerializer
from news_monitoring.source import services
from news_monitoring.story.models import Story


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
        user = self.request.user
        if user.is_staff:
            return Source.objects.all().prefetch_related('tagged_companies')
        return Source.objects.filter(company=user.company).prefetch_related('tagged_companies')

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

    # @action(detail=False, methods=['get'], url_path='form-data')
    # def get_source_form_data(self, request):
    #     """
    #     Returns company list and optionally source/tagged_companies for editing form
    #     """
    #     source_id = request.GET.get("source_id")
    #     source_obj = None
    #     tagged_companies = []
    #     companies = Company.objects.all()
    #
    #     if source_id:
    #         source_obj, tagged_companies = services.get_source(request.user, source_id)
    #         serializer = SourceSerializer(source_obj)
    #
    #         # Fix: Check if tagged_companies is a QuerySet or list
    #         if hasattr(tagged_companies, 'values_list'):
    #             # It's a QuerySet
    #             tagged_companies_ids = list(tagged_companies.values_list("id", flat=True))
    #         else:
    #             # It's already a list
    #             tagged_companies_ids = [company.id if hasattr(company, 'id') else company for company in
    #                                     tagged_companies]
    #     else:
    #         serializer = None
    #         tagged_companies_ids = []
    #
    #     return Response({
    #         "source": serializer.data if serializer else None,
    #         "companies": list(companies.values()),
    #         "tagged_companies": tagged_companies_ids,
    #     })

def index(request):
    return shortcuts.render(request, "source/index.html")
