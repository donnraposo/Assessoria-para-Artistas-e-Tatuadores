from rest_framework import serializers

from modules.marketing.application.services import CampaignService
from modules.marketing.infrastructure.persistence.models import Campaign


class CampaignSerializer(serializers.ModelSerializer):
    class Meta:
        model = Campaign
        exclude = ["created_by"]
        read_only_fields = ["id", "created_at", "updated_at"]

    def create(self, validated_data):
        return CampaignService.create(
            actor=self.context["request"].user,
            **validated_data,
        )
