from rest_framework import status
from rest_framework.request import Request
from rest_framework.response import Response
from rest_framework.views import APIView

from modules.guests.infrastructure.persistence.models import Guest
from modules.identity.domain.enums import RoleType

from ..serializers import GuestSerializer


class GuestCollectionView(APIView):
    def get(self, request: Request) -> Response:
        roles = set(request.user.roles.values_list("role__code", flat=True))
        guests = Guest.objects.select_related("artist", "proposal")
        if RoleType.ADVISORY in roles:
            pass
        elif RoleType.ARTIST in roles:
            guests = guests.filter(artist__user=request.user)
        else:
            return Response(
                {"detail": "This account cannot access Guests."},
                status=status.HTTP_403_FORBIDDEN,
            )
        return Response(GuestSerializer(guests, many=True).data)
