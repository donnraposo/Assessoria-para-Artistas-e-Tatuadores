from rest_framework import serializers

from modules.studios.infrastructure.persistence.models import StudioBookingRequest


class BookingRequestSerializer(serializers.ModelSerializer):
    class Meta:
        model = StudioBookingRequest
        exclude = ["requested_by"]
        read_only_fields = ["id", "status", "response_reason", "created_at", "updated_at"]

    def validate(self, attrs):
        if attrs["ends_at"] <= attrs["starts_at"]:
            raise serializers.ValidationError("The end time must be after the start time.")
        return attrs
