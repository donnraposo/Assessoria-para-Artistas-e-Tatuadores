from rest_framework import status
from rest_framework.request import Request
from rest_framework.response import Response
from rest_framework.views import APIView

from modules.guests.application.services import GuestTransitionService
from modules.guests.infrastructure.persistence.models import Guest
from modules.identity.presentation.api.permissions import HasAdvisoryRole

from ..serializers import GuestSerializer


class GuestTransitionView(APIView):
    permission_classes = [HasAdvisoryRole]

    def post(self, request: Request, guest_id) -> Response:
        guest = Guest.objects.get(pk=guest_id)
        try:
            guest = GuestTransitionService.transition(
                guest,
                str(request.data.get("status", "")),
                request.user,
                str(request.data.get("reason", "")),
            )
        except ValueError as error:
            return Response({"detail": str(error)}, status=status.HTTP_409_CONFLICT)
        return Response(GuestSerializer(guest).data)
