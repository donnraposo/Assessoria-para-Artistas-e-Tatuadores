from rest_framework import serializers

from modules.artists.infrastructure.persistence.models import ArtistProfile


class ArtistProfileSerializer(serializers.ModelSerializer):
    class Meta:
        model = ArtistProfile
        exclude = ["user"]
        read_only_fields = ["id", "created_at", "updated_at"]
