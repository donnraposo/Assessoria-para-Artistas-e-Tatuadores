from rest_framework import serializers

from modules.scheduling.infrastructure.persistence.models import CancellationRequest


class CancellationRequestSerializer(serializers.ModelSerializer):
    class Meta:
        model = CancellationRequest
        fields = [
            "id",
            "appointment",
            "requested_by",
            "responsibility",
            "reason",
            "status",
            "decided_by",
            "decision_reason",
            "created_at",
            "decided_at",
        ]
        read_only_fields = fields
