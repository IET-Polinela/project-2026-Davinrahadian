from rest_framework import serializers

from .models import Report
from usermanagement_24782084.models import User


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


class RegisterSerializer(serializers.ModelSerializer):
    password = serializers.CharField(write_only=True, min_length=8, style={'input_type': 'password'})
    password_confirm = serializers.CharField(write_only=True, style={'input_type': 'password'})

    class Meta:
        model = User
        fields = ['id', 'username', 'email', 'password', 'password_confirm']
        read_only_fields = ['id']

    def validate(self, attrs):
        if attrs['password'] != attrs['password_confirm']:
            raise serializers.ValidationError({'password_confirm': 'Password confirmation tidak cocok.'})
        return attrs

    def create(self, validated_data):
        validated_data.pop('password_confirm')
        password = validated_data.pop('password')

        user = User(
            **validated_data,
            is_admin=False,
            is_member=True,
        )
        user.set_password(password)
        user.save()
        return user
