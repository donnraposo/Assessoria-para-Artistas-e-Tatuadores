from rest_framework import status
from rest_framework.request import Request
from rest_framework.response import Response
from rest_framework.views import APIView

from modules.identity.presentation.api.permissions import HasAdvisoryRole
from modules.studios.application.services import StudioBookingService
from modules.studios.infrastructure.persistence.models import StudioBookingRequest


class BookingConfirmView(APIView):
    permission_classes = [HasAdvisoryRole]

    def post(self, request: Request, request_id) -> Response:
        booking_request = StudioBookingRequest.objects.get(pk=request_id)
        try:
            booking = StudioBookingService.confirm(booking_request, request.user)
        except ValueError as error:
            return Response({"detail": str(error)}, status=status.HTTP_409_CONFLICT)
        return Response({"id": booking.id, "status": booking.request.status}, status=201)
