from rest_framework import serializers

from modules.scheduling.application.services import AppointmentService
from modules.scheduling.infrastructure.persistence.models import Appointment


class AppointmentSerializer(serializers.ModelSerializer):
    class Meta:
        model = Appointment
        exclude = ["artist", "created_by"]
        read_only_fields = ["id", "final_value", "status", "created_at", "updated_at"]

    def create(self, validated_data):
        return AppointmentService.create(
            actor=self.context["request"].user,
            **validated_data,
        )
