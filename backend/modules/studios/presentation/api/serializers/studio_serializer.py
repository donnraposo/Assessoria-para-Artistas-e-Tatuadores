from rest_framework import serializers

from modules.studios.infrastructure.persistence.models import Studio


class StudioSerializer(serializers.ModelSerializer):
    class Meta:
        model = Studio
        exclude = ["owner", "reviewed_by"]
        read_only_fields = ["id", "status", "review_reason", "created_at", "updated_at"]
