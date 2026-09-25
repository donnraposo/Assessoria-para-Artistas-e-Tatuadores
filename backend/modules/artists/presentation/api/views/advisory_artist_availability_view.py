from rest_framework.request import Request
from rest_framework.response import Response
from rest_framework.views import APIView

from modules.artists.infrastructure.persistence.models import ArtistAvailability
from modules.identity.presentation.api.permissions import HasAdvisoryRole

from ..serializers import ArtistAvailabilitySerializer


class AdvisoryArtistAvailabilityView(APIView):
    permission_classes = [HasAdvisoryRole]

    def get(self, request: Request, artist_id) -> Response:
        availability = ArtistAvailability.objects.filter(artist_id=artist_id).order_by("starts_at")
        return Response(ArtistAvailabilitySerializer(availability, many=True).data)
