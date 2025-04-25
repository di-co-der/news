from django import shortcuts

from rest_framework import viewsets, permissions, status
from rest_framework.response import Response
from rest_framework import filters

from news_monitoring.story.models import Story
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
        queryset = Story.objects.prefetch_related('tagged_companies')
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
        return Response({"detail": "Story deleted successfully."}, status=status.HTTP_204_NO_CONTENT)

def angular_index(request):
    return shortcuts.render(request, "story/index.html")
