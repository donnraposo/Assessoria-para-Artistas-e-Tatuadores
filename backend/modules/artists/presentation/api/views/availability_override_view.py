from django.shortcuts import get_object_or_404
from rest_framework import status
from rest_framework.request import Request
from rest_framework.response import Response
from rest_framework.views import APIView

from modules.artists.application.services import ArtistAvailabilityService
from modules.artists.infrastructure.persistence.models import ArtistAvailability
from modules.identity.presentation.api.permissions import HasAdvisoryRole

from ..serializers import ArtistAvailabilitySerializer, AvailabilityOverrideSerializer


class AvailabilityOverrideView(APIView):
    permission_classes = [HasAdvisoryRole]

    def post(self, request: Request, availability_id) -> Response:
        serializer = AvailabilityOverrideSerializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        availability = get_object_or_404(ArtistAvailability, pk=availability_id)
        try:
            availability = ArtistAvailabilityService.override(
                availability=availability,
                actor=request.user,
                **serializer.validated_data,
            )
        except ValueError as error:
            return Response({"detail": str(error)}, status=status.HTTP_409_CONFLICT)
        return Response(ArtistAvailabilitySerializer(availability).data)
