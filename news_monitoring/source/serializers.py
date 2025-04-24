from rest_framework import serializers
from news_monitoring.source import models


#create serializers here
class SourceSerializer(serializers.ModelSerializer):
    companies = serializers.SerializerMethodField()

    class Meta:
        model = models.Source
        fields = ['id', 'name', 'url', 'companies', 'added_by', 'updated_by']

    def get_companies(self, obj):
        return [company.name for company in obj.tagged_companies.all()]
