from rest_framework import serializers
from drf_spectacular.utils import extend_schema_field

from .models import Report


class ReportSerializer(serializers.ModelSerializer):
    reporter = serializers.SerializerMethodField()
    is_owner = serializers.SerializerMethodField()
    reporter_name = serializers.SerializerMethodField()

    class Meta:
        model = Report
        fields = [
            'id', 'title', 'category', 'description',
            'location', 'status', 'reporter', 'reporter_name',
            'created_at', 'updated_at', 'is_owner',
        ]

    @extend_schema_field(serializers.CharField)
    def get_reporter(self, obj):
        request = self.context.get('request')
        if request and request.user.is_authenticated:
            if obj.reporter == request.user:
                return request.user.username
        return "Warga Anonim"

    @extend_schema_field(serializers.CharField)
    def get_reporter_name(self, obj):
        request = self.context.get('request')
        if request and request.user.is_authenticated and obj.reporter == request.user:
            return request.user.username
        return "Warga Anonim"

    @extend_schema_field(serializers.BooleanField)
    def get_is_owner(self, obj):
        request = self.context.get('request')
        if request and request.user.is_authenticated:
            return obj.reporter == request.user
        return False
