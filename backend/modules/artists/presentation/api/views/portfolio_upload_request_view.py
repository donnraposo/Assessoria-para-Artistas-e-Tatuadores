from rest_framework import status
from rest_framework.request import Request
from rest_framework.response import Response
from rest_framework.views import APIView

from modules.artists.application.services import PortfolioUploadService
from modules.artists.infrastructure.persistence.models import ArtistProfile
from modules.artists.presentation.api.serializers import PortfolioUploadRequestSerializer
from modules.identity.presentation.api.permissions import HasArtistRole


class PortfolioUploadRequestView(APIView):
    permission_classes = [HasArtistRole]

    def post(self, request: Request) -> Response:
        serializer = PortfolioUploadRequestSerializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        artist = ArtistProfile.objects.get(user=request.user)
        try:
            upload, upload_url = PortfolioUploadService.request(
                artist=artist,
                **serializer.validated_data,
            )
        except ValueError as error:
            return Response({"detail": str(error)}, status=status.HTTP_409_CONFLICT)
        return Response(
            {
                "upload_id": upload.id,
                "upload_url": upload_url,
                "expires_at": upload.expires_at,
            },
            status=status.HTTP_201_CREATED,
        )
