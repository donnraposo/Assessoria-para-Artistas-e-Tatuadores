from rest_framework import serializers

from modules.studios.infrastructure.persistence.models import Workstation


class WorkstationSerializer(serializers.ModelSerializer):
    class Meta:
        model = Workstation
        exclude = ["studio"]
        read_only_fields = ["id"]
