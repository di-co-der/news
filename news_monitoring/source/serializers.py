from rest_framework import serializers
from news_monitoring.source import models


#create serializers here
class SourceSerializer(serializers.ModelSerializer):
    # Field used for input/output of IDs
    tagged_companies = serializers.PrimaryKeyRelatedField(
        queryset=models.Company.objects.all(),
        many=True,
        required=False
    )

    # Field for display only (read-only)
    tagged_company_names = serializers.SerializerMethodField()

    class Meta:
        model = models.Source
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
