from rest_framework import serializers

from modules.studios.infrastructure.persistence.models import StudioAvailability


class StudioAvailabilitySerializer(serializers.ModelSerializer):
    class Meta:
        model = StudioAvailability
        exclude = ["studio"]
        read_only_fields = ["id"]

    def validate(self, attrs):
        if attrs["ends_at"] <= attrs["starts_at"]:
            raise serializers.ValidationError("The end time must be after the start time.")
        if attrs.get("capacity", 1) < 1:
            raise serializers.ValidationError("Capacity must be positive.")
        workstation = attrs.get("workstation")
        if workstation and workstation.studio_id != self.context["studio"].id:
            raise serializers.ValidationError("The workstation does not belong to this Studio.")
        return attrs
