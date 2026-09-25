from rest_framework import serializers

from modules.guests.infrastructure.persistence.models import GuestStudio


class GuestStudioSerializer(serializers.ModelSerializer):
    class Meta:
        model = GuestStudio
        fields = ["id", "guest", "studio", "starts_at", "ends_at", "created_at"]
        read_only_fields = ["id", "guest", "created_at"]
