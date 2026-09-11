from rest_framework import serializers

from modules.sales.infrastructure.persistence.models import Lead


class LeadSerializer(serializers.ModelSerializer):
    class Meta:
        model = Lead
        exclude = ["created_by"]
        read_only_fields = ["id", "status", "created_at", "updated_at"]

    def create(self, validated_data):
        return Lead.objects.create(
            created_by=self.context["request"].user,
            **validated_data,
        )
