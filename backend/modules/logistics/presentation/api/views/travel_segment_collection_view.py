from django.shortcuts import get_object_or_404
from rest_framework import status
from rest_framework.request import Request
from rest_framework.response import Response
from rest_framework.views import APIView

from modules.guests.infrastructure.persistence.models import Guest
from modules.identity.domain.enums import RoleType
from modules.logistics.infrastructure.persistence.models import TravelSegment
from modules.logistics.presentation.api.serializers import TravelSegmentSerializer


class TravelSegmentCollectionView(APIView):
    def get(self, request: Request, guest_id) -> Response:
        guest = get_object_or_404(Guest.objects.select_related("artist__user"), pk=guest_id)
        is_advisory = request.user.roles.filter(role__code=RoleType.ADVISORY).exists()
        if not is_advisory and guest.artist.user_id != request.user.id:
            return Response(
                {"detail": "You cannot access this Guest travel information."},
                status=status.HTTP_403_FORBIDDEN,
            )
        segments = TravelSegment.objects.filter(guest=guest)
        return Response(TravelSegmentSerializer(segments, many=True).data)

    def post(self, request: Request, guest_id) -> Response:
        if not request.user.roles.filter(role__code=RoleType.ADVISORY).exists():
            return Response(
                {"detail": "Only Advisory users can manage travel information."},
                status=status.HTTP_403_FORBIDDEN,
            )
        guest = get_object_or_404(Guest, pk=guest_id)
        serializer = TravelSegmentSerializer(
            data=request.data,
            context={"request": request, "guest": guest},
        )
        serializer.is_valid(raise_exception=True)
        try:
            serializer.save()
        except ValueError as error:
            return Response({"detail": str(error)}, status=status.HTTP_409_CONFLICT)
        return Response(serializer.data, status=status.HTTP_201_CREATED)
