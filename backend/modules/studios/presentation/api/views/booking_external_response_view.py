from rest_framework import status
from rest_framework.request import Request
from rest_framework.response import Response
from rest_framework.views import APIView

from modules.identity.presentation.api.permissions import HasAdvisoryRole
from modules.studios.application.services import StudioBookingService
from modules.studios.infrastructure.persistence.models import StudioBookingRequest

from ..serializers import BookingRequestSerializer


class BookingExternalResponseView(APIView):
    permission_classes = [HasAdvisoryRole]

    def post(self, request: Request, request_id) -> Response:
        booking_request = StudioBookingRequest.objects.get(pk=request_id)
        try:
            booking_request = StudioBookingService.register_external_response(
                booking_request,
                request.user,
                bool(request.data.get("accepted")),
                str(request.data.get("reason", "")),
            )
        except ValueError as error:
            return Response({"detail": str(error)}, status=status.HTTP_409_CONFLICT)
        return Response(BookingRequestSerializer(booking_request).data)
