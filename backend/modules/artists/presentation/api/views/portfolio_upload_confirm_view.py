from botocore.exceptions import BotoCoreError, ClientError
from django.shortcuts import get_object_or_404
from rest_framework import status
from rest_framework.request import Request
from rest_framework.response import Response
from rest_framework.views import APIView

from modules.artists.application.services import PortfolioUploadService
from modules.artists.infrastructure.persistence.models import PendingPortfolioUpload
from modules.artists.presentation.api.serializers import PortfolioItemSerializer
from modules.identity.presentation.api.permissions import HasArtistRole


class PortfolioUploadConfirmView(APIView):
    permission_classes = [HasArtistRole]

    def post(self, request: Request, upload_id) -> Response:
        upload = get_object_or_404(
            PendingPortfolioUpload.objects.select_related("artist"),
            pk=upload_id,
            artist__user=request.user,
        )
        try:
            item = PortfolioUploadService.confirm(upload=upload, actor=request.user)
        except ValueError as error:
            return Response({"detail": str(error)}, status=status.HTTP_409_CONFLICT)
        except (BotoCoreError, ClientError):
            return Response(
                {"detail": "The uploaded object is not available for confirmation."},
                status=status.HTTP_503_SERVICE_UNAVAILABLE,
            )
        return Response(PortfolioItemSerializer(item).data)
