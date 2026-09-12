from django.shortcuts import get_object_or_404
from rest_framework import status
from rest_framework.request import Request
from rest_framework.response import Response
from rest_framework.views import APIView

from modules.guests.infrastructure.persistence.models import Guest
from modules.identity.domain.enums import RoleType
from modules.logistics.application.services import MyTripService
from modules.logistics.presentation.api.serializers import (
    AccommodationSerializer,
    GuestStudioTripSerializer,
    MyTripAppointmentSerializer,
    TravelSegmentSerializer,
)


class MyTripView(APIView):
    def get(self, request: Request, guest_id) -> Response:
        guest = get_object_or_404(Guest.objects.select_related("artist__user"), pk=guest_id)
        is_advisory = request.user.roles.filter(role__code=RoleType.ADVISORY).exists()
        if not is_advisory and guest.artist.user_id != request.user.id:
            return Response(
                {"detail": "You cannot access this Guest trip."},
                status=status.HTTP_403_FORBIDDEN,
            )
        trip = MyTripService.build(guest)
        return Response(
            {
                "guest": {
                    "id": guest.id,
                    "city": guest.city,
                    "country_code": guest.country_code,
                    "starts_on": guest.starts_on,
                    "ends_on": guest.ends_on,
                    "timezone": guest.timezone,
                },
                "status": trip["status"],
                "travel_segments": TravelSegmentSerializer(trip["travel_segments"], many=True).data,
                "accommodations": AccommodationSerializer(trip["accommodations"], many=True).data,
                "studios": GuestStudioTripSerializer(trip["studios"], many=True).data,
                "appointments": MyTripAppointmentSerializer(trip["appointments"], many=True).data,
                "costs": trip["costs"],
            }
        )
