from rest_framework import status
from rest_framework.request import Request
from rest_framework.response import Response
from rest_framework.views import APIView

from modules.identity.presentation.api.permissions import HasArtistRole
from modules.scheduling.application.services import CancellationService
from modules.scheduling.infrastructure.persistence.models import Appointment
from modules.scheduling.presentation.api.serializers import (
    CancellationInputSerializer,
    CancellationRequestSerializer,
)


class CancellationRequestCreateView(APIView):
    permission_classes = [HasArtistRole]

    def post(self, request: Request, appointment_id) -> Response:
        serializer = CancellationInputSerializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        appointment = Appointment.objects.get(pk=appointment_id)
        try:
            cancellation = CancellationService.request(
                appointment=appointment,
                actor=request.user,
                reason=serializer.validated_data["reason"],
            )
        except ValueError as error:
            return Response({"detail": str(error)}, status=status.HTTP_409_CONFLICT)
        return Response(
            CancellationRequestSerializer(cancellation).data,
            status=status.HTTP_201_CREATED,
        )
