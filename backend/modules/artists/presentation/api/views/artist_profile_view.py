from rest_framework.request import Request
from rest_framework.response import Response
from rest_framework.views import APIView

from modules.artists.infrastructure.persistence.models import ArtistApplication, ArtistProfile
from modules.identity.presentation.api.permissions import HasArtistRole

from ..serializers import ArtistProfileSerializer


class ArtistProfileView(APIView):
    permission_classes = [HasArtistRole]

    def get(self, request: Request) -> Response:
        profile = ArtistProfile.objects.get(user=request.user)
        return Response(ArtistProfileSerializer(profile).data)

    def put(self, request: Request) -> Response:
        profile, created = ArtistProfile.objects.get_or_create(user=request.user)
        serializer = ArtistProfileSerializer(profile, data=request.data)
        serializer.is_valid(raise_exception=True)
        profile = serializer.save()
        if created:
            ArtistApplication.objects.create(artist=profile)
        return Response(serializer.data)
