from rest_framework import status
from rest_framework.request import Request
from rest_framework.response import Response
from rest_framework.views import APIView

from modules.identity.presentation.api.permissions import HasAdvisoryRole
from modules.studios.application.services import StudioBookingService
from modules.studios.infrastructure.persistence.models import StudioBooking

from ..serializers import BookingPaymentStatusSerializer


class BookingPaymentStatusView(APIView):
    permission_classes = [HasAdvisoryRole]

    def patch(self, request: Request, booking_id) -> Response:
        booking = StudioBooking.objects.get(pk=booking_id)
        serializer = BookingPaymentStatusSerializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        try:
            booking = StudioBookingService.update_payment_status(
                booking,
                request.user,
                serializer.validated_data["payment_status"],
            )
        except ValueError as error:
            return Response({"detail": str(error)}, status=status.HTTP_409_CONFLICT)
        return Response({"id": booking.id, "payment_status": booking.payment_status})
