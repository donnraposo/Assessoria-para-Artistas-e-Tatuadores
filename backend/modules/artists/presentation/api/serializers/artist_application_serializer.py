from rest_framework import serializers

from modules.artists.infrastructure.persistence.models import ArtistApplication


class ArtistApplicationSerializer(serializers.ModelSerializer):
    class Meta:
        model = ArtistApplication
        fields = ["id", "status", "review_reason", "submitted_at", "reviewed_at"]
        read_only_fields = fields
