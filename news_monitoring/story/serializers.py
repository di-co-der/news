from rest_framework import serializers

from news_monitoring.company.models import Company
from news_monitoring.story.models import Story
from news_monitoring.company import serializers as company_serializers


class StorySerializer(serializers.ModelSerializer):
    tagged_companies = serializers.PrimaryKeyRelatedField(
        many=True,
        queryset=Company.objects.all(),
        required=False
    )

    class Meta:
        model = Story
        fields = ['id', 'published_date', 'title', 'body_text', 'article_url', 'tagged_companies', 'added_by', 'updated_by']

    def to_representation(self, instance):
        representation = super().to_representation(instance)
        representation['tagged_companies'] = company_serializers.CompanySerializer(
            instance.tagged_companies.all(),
            many=True
        ).data
        return representation
