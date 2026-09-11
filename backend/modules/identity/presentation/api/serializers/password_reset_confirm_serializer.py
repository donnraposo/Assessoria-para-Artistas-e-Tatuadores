from django.contrib.auth.password_validation import validate_password
from rest_framework import serializers


class PasswordResetConfirmSerializer(serializers.Serializer):
    uid = serializers.CharField()
    token = serializers.CharField()
    password = serializers.CharField(write_only=True, trim_whitespace=False)

    def validate_password(self, value: str) -> str:
        validate_password(value)
        return value
