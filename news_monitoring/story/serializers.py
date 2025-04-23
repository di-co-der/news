from rest_framework import serializers
from news_monitoring.story.models import Story
from news_monitoring.company.models import Company


class StorySerializer(serializers.ModelSerializer):
    source_details = serializers.SerializerMethodField(read_only=True)
    tagged_companies = serializers.PrimaryKeyRelatedField(
        queryset=Company.objects.all(),
        many=True,
        required=False
    )

    # Field for display only (read-only)
    tagged_company_names = serializers.SerializerMethodField()

    class Meta:
        model = Story
        fields = '__all__'

    def get_tagged_company_names(self, obj):
        # This will return a list of company names instead of just IDs
        return [company.name for company in obj.tagged_companies.all()]

    def to_representation(self, instance):
        # Override to return names in the 'tagged_companies' field for display
        rep = super().to_representation(instance)
        # Replace the IDs with names for the tagged_companies field
        rep['tagged_companies'] = self.get_tagged_company_names(instance)
        return rep

    def get_source_details(self, obj):
        # Returns source details if a source exists
        if obj.source:
            return {
                "id": obj.source.id,
                "name": obj.source.name,
                # Using a more generic url field that should exist in your Source model
                "url": obj.source.url if hasattr(obj.source, 'url') else None
            }
        return None

    def get_company_name(self, obj):
        # Returns the primary company name
        return obj.company.name if obj.company else None
