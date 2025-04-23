# company/serializers.py
from rest_framework import serializers
from .models import Company

class CompanySerializer(serializers.ModelSerializer):
    class Meta:
        model = Company
        fields = ['id', 'name', 'domain', 'added_on', 'updated_on']
        read_only_fields = ['added_by', 'updated_by', 'added_on', 'updated_on']
