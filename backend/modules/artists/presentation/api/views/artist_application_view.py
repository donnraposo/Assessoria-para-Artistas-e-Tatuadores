from rest_framework import status
from rest_framework.request import Request
from rest_framework.response import Response
from rest_framework.views import APIView

from modules.artists.application.services import ArtistApplicationService
from modules.artists.infrastructure.persistence.models import ArtistApplication, ArtistProfile
from modules.identity.presentation.api.permissions import HasArtistRole

from ..serializers import ArtistApplicationSerializer


class ArtistApplicationView(APIView):
    permission_classes = [HasArtistRole]

    def get(self, request: Request) -> Response:
        profile = ArtistProfile.objects.get(user=request.user)
        application, _ = ArtistApplication.objects.get_or_create(artist=profile)
        return Response(ArtistApplicationSerializer(application).data)

    def post(self, request: Request) -> Response:
        profile = ArtistProfile.objects.get(user=request.user)
        application, _ = ArtistApplication.objects.get_or_create(artist=profile)
        try:
            ArtistApplicationService.submit(application)
        except ValueError as error:
            return Response({"detail": str(error)}, status=status.HTTP_409_CONFLICT)
        return Response(ArtistApplicationSerializer(application).data)
