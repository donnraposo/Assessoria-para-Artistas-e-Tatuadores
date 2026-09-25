from rest_framework import serializers

from modules.studios.infrastructure.persistence.models import Studio


class GuestStudioInputSerializer(serializers.Serializer):
    studio = serializers.PrimaryKeyRelatedField(queryset=Studio.objects.all())
    starts_at = serializers.DateTimeField()
    ends_at = serializers.DateTimeField()
