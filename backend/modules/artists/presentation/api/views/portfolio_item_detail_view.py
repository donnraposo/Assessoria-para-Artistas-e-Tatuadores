from botocore.exceptions import BotoCoreError, ClientError
from django.shortcuts import get_object_or_404
from rest_framework import status
from rest_framework.request import Request
from rest_framework.response import Response
from rest_framework.views import APIView

from modules.artists.application.services import PortfolioUploadService
from modules.artists.infrastructure.persistence.models import PortfolioItem
from modules.identity.presentation.api.permissions import HasArtistRole


class PortfolioItemDetailView(APIView):
    permission_classes = [HasArtistRole]

    def delete(self, request: Request, item_id) -> Response:
        item = get_object_or_404(PortfolioItem, pk=item_id, artist__user=request.user)
        try:
            PortfolioUploadService.delete(item=item, actor=request.user)
        except (BotoCoreError, ClientError):
            return Response(
                {"detail": "The portfolio image could not be removed from private storage."},
                status=status.HTTP_503_SERVICE_UNAVAILABLE,
            )
        return Response(status=status.HTTP_204_NO_CONTENT)
