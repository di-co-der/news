from rest_framework import serializers

from news_monitoring.company.models import Company
from news_monitoring.source import models
from news_monitoring.company import serializers as company_serializers


class SourceSerializer(serializers.ModelSerializer):
    tagged_companies = serializers.PrimaryKeyRelatedField(
        many=True,
        queryset=Company.objects.all(),
        required=False
    )

    class Meta:
        model = models.Source
        fields = ['id', 'name', 'url', 'tagged_companies', 'added_by', 'updated_by']

    def to_representation(self, instance):
        representation = super().to_representation(instance)
        representation['tagged_companies'] = company_serializers.CompanySerializer(
            instance.tagged_companies.all(),
            many=True
        ).data
        return representation
