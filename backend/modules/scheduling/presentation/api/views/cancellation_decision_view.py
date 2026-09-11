from rest_framework import status
from rest_framework.request import Request
from rest_framework.response import Response
from rest_framework.views import APIView

from modules.identity.presentation.api.permissions import HasAdvisoryRole
from modules.scheduling.application.services import CancellationService
from modules.scheduling.infrastructure.persistence.models import CancellationRequest
from modules.scheduling.presentation.api.serializers import (
    CancellationDecisionSerializer,
    CancellationRequestSerializer,
)


class CancellationDecisionView(APIView):
    permission_classes = [HasAdvisoryRole]

    def post(self, request: Request, cancellation_id) -> Response:
        serializer = CancellationDecisionSerializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        cancellation = CancellationRequest.objects.get(pk=cancellation_id)
        try:
            cancellation = CancellationService.decide(
                cancellation=cancellation,
                actor=request.user,
                **serializer.validated_data,
            )
        except ValueError as error:
            return Response({"detail": str(error)}, status=status.HTTP_409_CONFLICT)
        return Response(CancellationRequestSerializer(cancellation).data)
