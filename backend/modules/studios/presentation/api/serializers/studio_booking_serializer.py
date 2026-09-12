from rest_framework import serializers

from modules.studios.infrastructure.persistence.models import StudioBooking


class StudioBookingSerializer(serializers.ModelSerializer):
    studio = serializers.PrimaryKeyRelatedField(source="request.studio", read_only=True)
    workstation = serializers.PrimaryKeyRelatedField(source="request.workstation", read_only=True)
    starts_at = serializers.DateTimeField(source="request.starts_at", read_only=True)
    ends_at = serializers.DateTimeField(source="request.ends_at", read_only=True)
    timezone = serializers.CharField(source="request.timezone", read_only=True)

    class Meta:
        model = StudioBooking
        fields = [
            "id",
            "studio",
            "workstation",
            "starts_at",
            "ends_at",
            "timezone",
            "payment_status",
            "confirmed_at",
        ]
