from django import shortcuts

from rest_framework import viewsets, permissions, status
from rest_framework.response import Response
from rest_framework.decorators import action
from rest_framework import filters

from news_monitoring.company.models import Company
from news_monitoring.source.models import Source
from news_monitoring.source.serializers import SourceSerializer
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
        user = self.request.user
        # For staff users, show all sources
        if user.is_staff:
            return Source.objects.all()
        # For normal users, show sources assigned to their company
        return Source.objects.filter(company=user.company)

    def perform_create(self, serializer):
        # Make sure to set the company to the user's company if not provided
        company = serializer.validated_data.get('company')
        if not company:
            company = self.request.user.company
        serializer.save(added_by=self.request.user, company=company)

    def perform_update(self, serializer):
        # Make sure to set the company to the user's company if not provided
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
        Custom action to import stories from a feed
        """
        source_obj, _ = services.get_source(request.user, pk)
        services.import_stories_from_feed(source_obj, request.user)
        return Response({"detail": "Stories imported successfully."})

    @action(detail=False, methods=['get'], url_path='search')
    def fetch_sources(self, request):
        """
        Custom action for searching sources with pagination
        """
        search_query = request.GET.get('q', '').strip()
        page_number = request.GET.get('page')
        sources_qs = services.get_sources(request.user, search_query)
        return services.get_sources_json(sources_qs, page_number)

    @action(detail=False, methods=['get'], url_path='form-data')
    def get_source_form_data(self, request):
        """
        Returns company list and optionally source/tagged_companies for editing form
        """
        source_id = request.GET.get("source_id")
        source_obj = None
        tagged_companies = []
        companies = Company.objects.all()

        if source_id:
            source_obj, tagged_companies = services.get_source(request.user, source_id)
            serializer = SourceSerializer(source_obj)

            # Fix: Check if tagged_companies is a QuerySet or list
            if hasattr(tagged_companies, 'values_list'):
                # It's a QuerySet
                tagged_companies_ids = list(tagged_companies.values_list("id", flat=True))
            else:
                # It's already a list
                tagged_companies_ids = [company.id if hasattr(company, 'id') else company for company in
                                        tagged_companies]
        else:
            serializer = None
            tagged_companies_ids = []

        return Response({
            "source": serializer.data if serializer else None,
            "companies": list(companies.values()),
            "tagged_companies": tagged_companies_ids,
        })

def angular_index(request, path=''):
    return shortcuts.render(request, "source/index.html")
