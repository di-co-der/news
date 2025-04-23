from django import shortcuts

from rest_framework import viewsets, permissions, status
from rest_framework.decorators import action
from rest_framework.response import Response
from rest_framework import filters

from news_monitoring.story.models import Story
from news_monitoring.company.models import Company
from news_monitoring.story import services
from news_monitoring.story.serializers import StorySerializer


class StoryViewSet(viewsets.ModelViewSet):
    """
    Handles listing, creating, updating, deleting stories
    with custom actions for searching and retrieving form data.
    """
    serializer_class = StorySerializer
    permission_classes = [permissions.IsAuthenticated]
    filter_backends = [filters.SearchFilter]
    search_fields = ['body_text']

    def get_queryset(self):
        user = self.request.user
        # For staff users, show all sources
        if user.is_staff:
            return Story.objects.all()
        # For normal users, show sources assigned to their company
        return Story.objects.filter(company=user.company)

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
        return Response({"detail": "Story deleted successfully."}, status=status.HTTP_204_NO_CONTENT)

    @action(detail=False, methods=['get'], url_path='search')
    def fetch_stories(self, request):
        """
        Custom action for searching stories with pagination
        """
        search_query = request.GET.get('q', '').strip()
        filter_date = request.GET.get('date', '').strip()
        page_number = request.GET.get('page')
        source_id = request.GET.get('source_id')

        stories_qs = services.get_stories(request.user, search_query, filter_date, source_id)
        return Response(services.get_stories_json(stories_qs, page_number))

    @action(detail=False, methods=['get'], url_path='form-data')
    def get_story_form_data(self, request):
        """
        Returns company list and optionally story/tagged_companies for editing form
        """
        story_id = request.GET.get("story_id")
        story_obj = None
        tagged_companies = []
        companies = Company.objects.all()

        if story_id:
            story_obj, tagged_companies = services.get_story(request.user, story_id)
            serializer = StorySerializer(story_obj)

            # Check if tagged_companies is a QuerySet or list
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
            "story": serializer.data if serializer else None,
            "companies": list(companies.values()),
            "tagged_companies": tagged_companies_ids,
        })

def angular_index(request, path=''):
    return shortcuts.render(request, "story/index.html")
