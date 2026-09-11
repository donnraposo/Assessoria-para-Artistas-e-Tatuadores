from rest_framework.request import Request
from rest_framework.response import Response
from rest_framework.views import APIView

from modules.artists.infrastructure.persistence.models import ArtistProfile, PortfolioItem
from modules.identity.presentation.api.permissions import HasArtistRole

from ..serializers import PortfolioItemSerializer


class PortfolioCollectionView(APIView):
    permission_classes = [HasArtistRole]

    def get(self, request: Request) -> Response:
        items = PortfolioItem.objects.filter(artist__user=request.user)
        return Response(PortfolioItemSerializer(items, many=True).data)

    def post(self, request: Request) -> Response:
        artist = ArtistProfile.objects.get(user=request.user)
        serializer = PortfolioItemSerializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        serializer.save(artist=artist)
        return Response(serializer.data, status=201)
