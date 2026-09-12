from rest_framework.request import Request
from rest_framework.response import Response
from rest_framework.views import APIView

from modules.artists.infrastructure.persistence.models import PortfolioItem
from modules.identity.presentation.api.permissions import HasArtistRole

from ..serializers import PortfolioItemSerializer


class PortfolioCollectionView(APIView):
    permission_classes = [HasArtistRole]

    def get(self, request: Request) -> Response:
        items = PortfolioItem.objects.filter(artist__user=request.user)
        return Response(PortfolioItemSerializer(items, many=True).data)
