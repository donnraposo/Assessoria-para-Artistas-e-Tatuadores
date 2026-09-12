from rest_framework import serializers

from modules.guests.infrastructure.persistence.models import GuestStudio


class GuestStudioTripSerializer(serializers.ModelSerializer):
    studio_name = serializers.CharField(source="studio.name", read_only=True)
    studio_address = serializers.CharField(source="studio.address", read_only=True)

    class Meta:
        model = GuestStudio
        fields = ["id", "studio", "studio_name", "studio_address", "starts_at", "ends_at"]
