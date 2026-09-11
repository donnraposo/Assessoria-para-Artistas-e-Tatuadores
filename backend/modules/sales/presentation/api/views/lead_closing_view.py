from rest_framework import status
from rest_framework.request import Request
from rest_framework.response import Response
from rest_framework.views import APIView

from modules.identity.presentation.api.permissions import HasAdvisoryRole
from modules.sales.application.services import ClosingService
from modules.sales.infrastructure.persistence.models import Lead
from modules.sales.presentation.api.serializers import ClosingRequestSerializer, ClosingSerializer
from modules.scheduling.infrastructure.persistence.models import Appointment


class LeadClosingView(APIView):
    permission_classes = [HasAdvisoryRole]

    def post(self, request: Request, lead_id) -> Response:
        serializer = ClosingRequestSerializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        lead = Lead.objects.get(pk=lead_id)
        appointment = Appointment.objects.get(pk=serializer.validated_data.pop("appointment_id"))
        try:
            closing = ClosingService.close(
                lead=lead,
                appointment=appointment,
                actor=request.user,
                **serializer.validated_data,
            )
        except ValueError as error:
            return Response({"detail": str(error)}, status=status.HTTP_409_CONFLICT)
        return Response(ClosingSerializer(closing).data, status=status.HTTP_201_CREATED)
