from rest_framework import serializers

from modules.guests.infrastructure.persistence.models import GuestProposal


class GuestProposalSerializer(serializers.ModelSerializer):
    class Meta:
        model = GuestProposal
        fields = "__all__"
        read_only_fields = ["id", "status", "created_at", "updated_at"]

    def validate(self, attrs):
        if attrs["ends_on"] < attrs["starts_on"]:
            raise serializers.ValidationError("The end date must not precede the start date.")
        if attrs["currency"] != attrs["currency"].upper():
            raise serializers.ValidationError("Currency must use an uppercase ISO 4217 code.")
        return attrs
