from rest_framework import status
from rest_framework.request import Request
from rest_framework.response import Response
from rest_framework.views import APIView

from modules.identity.presentation.api.permissions import HasStudioRole
from modules.studios.application.services import StudioBookingService
from modules.studios.infrastructure.persistence.models import StudioBookingRequest

from ..serializers import BookingRequestSerializer


class BookingResponseView(APIView):
    permission_classes = [HasStudioRole]

    def post(self, request: Request, request_id) -> Response:
        booking_request = StudioBookingRequest.objects.get(
            pk=request_id,
            studio__owner=request.user,
        )
        try:
            StudioBookingService.respond(
                booking_request,
                bool(request.data.get("accepted")),
                str(request.data.get("reason", "")),
            )
        except ValueError as error:
            return Response({"detail": str(error)}, status=status.HTTP_409_CONFLICT)
        return Response(BookingRequestSerializer(booking_request).data)
