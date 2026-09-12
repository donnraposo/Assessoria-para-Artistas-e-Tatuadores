from django.shortcuts import get_object_or_404
from rest_framework.request import Request
from rest_framework.response import Response
from rest_framework.views import APIView

from modules.artists.infrastructure.persistence.models import PortfolioItem
from modules.artists.infrastructure.storage import PortfolioStorage
from modules.identity.presentation.api.permissions import HasArtistRole


class PortfolioItemAccessView(APIView):
    permission_classes = [HasArtistRole]

    def get(self, request: Request, item_id) -> Response:
        item = get_object_or_404(PortfolioItem, pk=item_id, artist__user=request.user)
        return Response({"access_url": PortfolioStorage().create_download_url(item.object_key)})
