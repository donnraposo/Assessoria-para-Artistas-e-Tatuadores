from rest_framework.request import Request
from rest_framework.response import Response
from rest_framework.views import APIView

from modules.identity.presentation.api.permissions import HasStudioRole
from modules.studios.infrastructure.persistence.models import StudioBookingRequest

from ..serializers import BookingRequestSerializer


class StudioBookingRequestCollectionView(APIView):
    permission_classes = [HasStudioRole]

    def get(self, request: Request) -> Response:
        requests = StudioBookingRequest.objects.filter(
            studio__owner=request.user,
        ).select_related("guest", "artist", "studio")
        return Response(BookingRequestSerializer(requests, many=True).data)
