from rest_framework import serializers
from news_monitoring.source import models
from news_monitoring.company import serializers as company_serializers


class SourceSerializer(serializers.ModelSerializer):
    tagged_companies = company_serializers.CompanySerializer(many=True, read_only=True)

    class Meta:
        model = models.Source
        fields = ['id', 'name', 'url', 'tagged_companies', 'added_by', 'updated_by']
