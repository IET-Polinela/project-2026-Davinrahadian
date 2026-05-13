from rest_framework import serializers

from .models import Report


class ReportSerializer(serializers.ModelSerializer):
    reporter = serializers.SerializerMethodField()

    class Meta:
        model = Report
        fields = [
            'id',
            'title',
            'reporter',
            'category',
            'location',
            'description',
            'status',
            'created_at',
            'updated_at',
        ]

    def get_reporter(self, obj):
        return 'Warga Anonim'
