from django.contrib.auth.password_validation import validate_password
from django.core.exceptions import ValidationError as DjangoValidationError
from rest_framework import serializers

from modules.identity.domain.enums import RoleType
from modules.identity.infrastructure.persistence.models import User


class RegistrationSerializer(serializers.Serializer):
    email = serializers.EmailField()
    password = serializers.CharField(write_only=True, trim_whitespace=False)
    full_name = serializers.CharField(max_length=160)
    role = serializers.ChoiceField(
        choices=[
            (RoleType.ARTIST, RoleType.ARTIST.label),
            (RoleType.STUDIO, RoleType.STUDIO.label),
        ]
    )

    def validate_email(self, value: str) -> str:
        normalized = value.strip().lower()
        if User.objects.filter(email=normalized).exists():
            raise serializers.ValidationError("An account with this email already exists.")
        return normalized

    def validate(self, attrs):
        temp_user = User(email=attrs["email"], full_name=attrs["full_name"])
        try:
            validate_password(attrs["password"], user=temp_user)
        except DjangoValidationError as error:
            raise serializers.ValidationError({"password": error.messages}) from error
        return attrs
