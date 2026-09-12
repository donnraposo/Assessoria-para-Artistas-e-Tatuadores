from django.db import transaction
from rest_framework import status
from rest_framework.request import Request
from rest_framework.response import Response
from rest_framework.views import APIView

from modules.artists.infrastructure.persistence.models import ArtistApplication, ArtistProfile
from modules.identity.presentation.api.permissions import HasArtistRole

from ..serializers import ArtistProfileSerializer


class ArtistProfileView(APIView):
    permission_classes = [HasArtistRole]

    def get(self, request: Request) -> Response:
        profile = ArtistProfile.objects.filter(user=request.user).first()
        if profile is None:
            return Response(
                {"detail": "The artist profile was not created yet."},
                status=status.HTTP_404_NOT_FOUND,
            )
        return Response(ArtistProfileSerializer(profile).data)

    @transaction.atomic
    def put(self, request: Request) -> Response:
        profile = ArtistProfile.objects.filter(user=request.user).first()
        serializer = ArtistProfileSerializer(profile, data=request.data)
        serializer.is_valid(raise_exception=True)
        profile = serializer.save(user=request.user)
        ArtistApplication.objects.get_or_create(artist=profile)
        return Response(serializer.data)
