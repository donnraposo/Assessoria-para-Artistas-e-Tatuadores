from rest_framework import serializers

from modules.artists.infrastructure.persistence.models import PortfolioItem


class PortfolioItemSerializer(serializers.ModelSerializer):
    class Meta:
        model = PortfolioItem
        fields = [
            "id",
            "original_name",
            "content_type",
            "size_bytes",
            "caption",
            "style",
            "position",
            "created_at",
        ]
        read_only_fields = fields
