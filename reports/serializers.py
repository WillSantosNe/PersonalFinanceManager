from rest_framework import serializers
from .models import Report

class ReportSerializer(serializers.ModelSerializer):
    class Meta:
        model = Report
        fields = ['id', 'user', 'format', 'created_at', 'file']
        read_only_fields = ['id', 'user', 'created_at', 'file']
