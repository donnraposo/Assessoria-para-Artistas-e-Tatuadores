from rest_framework import serializers

from modules.sales.infrastructure.persistence.models import Closing


class ClosingSerializer(serializers.ModelSerializer):
    agency_amount = serializers.DecimalField(
        source="agency_receipt.amount",
        max_digits=12,
        decimal_places=2,
        read_only=True,
    )
    payment_reference = serializers.CharField(
        source="agency_receipt.external_reference",
        read_only=True,
    )

    class Meta:
        model = Closing
        fields = [
            "id",
            "lead",
            "appointment",
            "final_value",
            "currency",
            "artist_minimum_approved",
            "agency_amount",
            "payment_reference",
            "closed_by",
            "closed_at",
        ]
        read_only_fields = fields
