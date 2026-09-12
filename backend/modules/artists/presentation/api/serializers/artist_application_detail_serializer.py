from rest_framework import serializers

from modules.artists.infrastructure.persistence.models import ArtistApplication, PortfolioItem

from .artist_profile_serializer import ArtistProfileSerializer
from .portfolio_item_serializer import PortfolioItemSerializer


class ArtistApplicationDetailSerializer(serializers.ModelSerializer):
    artist = ArtistProfileSerializer(read_only=True)
    contact_name = serializers.CharField(source="artist.user.full_name", read_only=True)
    contact_email = serializers.EmailField(source="artist.user.email", read_only=True)
    portfolio = serializers.SerializerMethodField()

    class Meta:
        model = ArtistApplication
        fields = [
            "id",
            "status",
            "review_reason",
            "submitted_at",
            "reviewed_at",
            "artist",
            "contact_name",
            "contact_email",
            "portfolio",
        ]
        read_only_fields = fields

    def get_portfolio(self, application: ArtistApplication) -> list[dict]:
        items = PortfolioItem.objects.filter(artist=application.artist).order_by(
            "position",
            "created_at",
        )
        return PortfolioItemSerializer(items, many=True).data
