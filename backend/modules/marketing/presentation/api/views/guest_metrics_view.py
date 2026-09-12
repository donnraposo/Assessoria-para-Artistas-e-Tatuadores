from rest_framework import status
from rest_framework.request import Request
from rest_framework.response import Response
from rest_framework.views import APIView

from modules.guests.infrastructure.persistence.models import Guest
from modules.identity.domain.enums import RoleType
from modules.marketing.application.services import MetricsService


class GuestMetricsView(APIView):
    def get(self, request: Request, guest_id) -> Response:
        guest = Guest.objects.select_related("artist__user").get(pk=guest_id)
        is_advisory = request.user.roles.filter(role__code=RoleType.ADVISORY).exists()
        if not is_advisory and guest.artist.user_id != request.user.id:
            return Response(
                {"detail": "You cannot access this Guest metrics."},
                status=status.HTTP_403_FORBIDDEN,
            )
        return Response(MetricsService.calculate(guest))
