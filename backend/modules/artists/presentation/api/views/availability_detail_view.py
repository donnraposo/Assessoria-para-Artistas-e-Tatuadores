from django.shortcuts import get_object_or_404
from rest_framework import status
from rest_framework.request import Request
from rest_framework.response import Response
from rest_framework.views import APIView

from modules.artists.application.services import ArtistAvailabilityService
from modules.artists.infrastructure.persistence.models import ArtistAvailability
from modules.identity.presentation.api.permissions import HasArtistRole

from ..serializers import ArtistAvailabilitySerializer


class AvailabilityDetailView(APIView):
    permission_classes = [HasArtistRole]

    def patch(self, request: Request, availability_id) -> Response:
        availability = get_object_or_404(
            ArtistAvailability, pk=availability_id, artist__user=request.user
        )
        serializer = ArtistAvailabilitySerializer(
            availability,
            data=request.data,
            context={"artist": availability.artist},
        )
        serializer.is_valid(raise_exception=True)
        try:
            updated = ArtistAvailabilityService.update(
                availability,
                serializer.validated_data["starts_at"],
                serializer.validated_data["ends_at"],
                serializer.validated_data["timezone"],
            )
        except ValueError as error:
            return Response({"detail": str(error)}, status=status.HTTP_409_CONFLICT)
        return Response(ArtistAvailabilitySerializer(updated).data)

    def delete(self, request: Request, availability_id) -> Response:
        availability = get_object_or_404(
            ArtistAvailability, pk=availability_id, artist__user=request.user
        )
        try:
            ArtistAvailabilityService.delete(availability)
        except ValueError as error:
            return Response({"detail": str(error)}, status=status.HTTP_409_CONFLICT)
        return Response(status=status.HTTP_204_NO_CONTENT)
