from rest_framework import status
from rest_framework.request import Request
from rest_framework.response import Response
from rest_framework.views import APIView

from modules.artists.application.services import ArtistAvailabilityService
from modules.artists.infrastructure.persistence.models import ArtistProfile
from modules.identity.presentation.api.permissions import HasAdvisoryRole

from ..serializers import AdvisoryAvailabilityOverrideSerializer, ArtistAvailabilitySerializer


class AdvisoryAvailabilityOverrideView(APIView):
    permission_classes = [HasAdvisoryRole]

    def post(self, request: Request, artist_id) -> Response:
        artist = ArtistProfile.objects.get(pk=artist_id)
        input_serializer = AdvisoryAvailabilityOverrideSerializer(data=request.data)
        input_serializer.is_valid(raise_exception=True)
        try:
            availability = ArtistAvailabilityService.override_by_advisory(
                artist=artist,
                actor=request.user,
                **input_serializer.validated_data,
            )
        except ValueError as error:
            return Response({"detail": str(error)}, status=status.HTTP_409_CONFLICT)
        return Response(
            ArtistAvailabilitySerializer(availability).data,
            status=status.HTTP_201_CREATED,
        )
