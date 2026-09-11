from rest_framework import status
from rest_framework.request import Request
from rest_framework.response import Response
from rest_framework.views import APIView

from modules.identity.domain.enums import RoleType
from modules.identity.presentation.api.permissions import HasAdvisoryRole
from modules.scheduling.infrastructure.persistence.models import Appointment
from modules.scheduling.presentation.api.serializers import AppointmentSerializer


class AppointmentCollectionView(APIView):
    def get(self, request: Request) -> Response:
        appointments = Appointment.objects.select_related("guest", "artist", "studio")
        if not request.user.roles.filter(role__code=RoleType.ADVISORY).exists():
            appointments = appointments.filter(artist__user=request.user)
        return Response(AppointmentSerializer(appointments, many=True).data)

    def post(self, request: Request) -> Response:
        permission = HasAdvisoryRole()
        if not permission.has_permission(request, self):
            return Response(
                {"detail": "Only Advisory users can create appointments."},
                status=status.HTTP_403_FORBIDDEN,
            )
        serializer = AppointmentSerializer(data=request.data, context={"request": request})
        serializer.is_valid(raise_exception=True)
        try:
            serializer.save()
        except ValueError as error:
            return Response({"detail": str(error)}, status=status.HTTP_409_CONFLICT)
        return Response(serializer.data, status=status.HTTP_201_CREATED)
