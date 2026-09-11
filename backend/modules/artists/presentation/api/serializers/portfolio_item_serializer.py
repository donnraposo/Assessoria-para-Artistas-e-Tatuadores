from rest_framework import serializers

from modules.artists.infrastructure.persistence.models import PortfolioItem


class PortfolioItemSerializer(serializers.ModelSerializer):
    class Meta:
        model = PortfolioItem
        exclude = ["artist"]
        read_only_fields = ["id", "created_at"]

    def validate_content_type(self, value: str) -> str:
        if value not in {"image/jpeg", "image/png", "image/webp"}:
            raise serializers.ValidationError("Unsupported image format.")
        return value

    def validate_size_bytes(self, value: int) -> int:
        if value > 10 * 1024 * 1024:
            raise serializers.ValidationError("The image must not exceed 10 MB.")
        return value
