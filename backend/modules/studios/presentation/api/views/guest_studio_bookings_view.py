from rest_framework.request import Request
from rest_framework.response import Response
from rest_framework.views import APIView

from modules.identity.presentation.api.permissions import HasAdvisoryRole
from modules.studios.infrastructure.persistence.models import StudioBooking

from ..serializers import StudioBookingSerializer


class GuestStudioBookingsView(APIView):
    permission_classes = [HasAdvisoryRole]

    def get(self, request: Request, guest_id) -> Response:
        bookings = StudioBooking.objects.filter(
            request__guest_id=guest_id
        ).select_related("request")
        return Response(StudioBookingSerializer(bookings, many=True).data)
