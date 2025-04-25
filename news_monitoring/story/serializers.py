from rest_framework import serializers
from news_monitoring.story.models import Story
from news_monitoring.company import serializers as company_serializers


class StorySerializer(serializers.ModelSerializer):
    tagged_companies = company_serializers.CompanySerializer(many=True, read_only=True)

    class Meta:
        model = Story
        fields = ['id', 'published_date', 'title', 'body_text', 'article_url', 'tagged_companies', 'added_by', 'updated_by']
