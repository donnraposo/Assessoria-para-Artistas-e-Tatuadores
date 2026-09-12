from rest_framework import serializers

from modules.marketing.application.services import CampaignService
from modules.marketing.infrastructure.persistence.models import AdSpend


class AdSpendSerializer(serializers.ModelSerializer):
    class Meta:
        model = AdSpend
        exclude = ["campaign", "recorded_by"]
        read_only_fields = ["id", "created_at"]

    def create(self, validated_data):
        return CampaignService.add_spend(
            campaign=self.context["campaign"],
            actor=self.context["request"].user,
            **validated_data,
        )
