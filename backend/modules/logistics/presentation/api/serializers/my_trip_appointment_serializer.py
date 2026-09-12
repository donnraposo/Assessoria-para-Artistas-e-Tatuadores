from rest_framework import serializers

from modules.scheduling.infrastructure.persistence.models import Appointment


class MyTripAppointmentSerializer(serializers.ModelSerializer):
    studio_name = serializers.CharField(source="studio.name", read_only=True)

    class Meta:
        model = Appointment
        fields = ["id", "starts_at", "ends_at", "timezone", "studio", "studio_name", "status"]
