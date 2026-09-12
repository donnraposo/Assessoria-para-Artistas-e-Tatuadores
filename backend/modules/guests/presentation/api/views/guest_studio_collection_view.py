from rest_framework import status
from rest_framework.request import Request
from rest_framework.response import Response
from rest_framework.views import APIView

from modules.guests.application.services import GuestStudioService
from modules.guests.infrastructure.persistence.models import Guest, GuestStudio
from modules.identity.presentation.api.permissions import HasAdvisoryRole

from ..serializers import GuestStudioInputSerializer, GuestStudioSerializer


class GuestStudioCollectionView(APIView):
    permission_classes = [HasAdvisoryRole]

    def get(self, request: Request, guest_id) -> Response:
        guest = Guest.objects.get(pk=guest_id)
        studios = GuestStudio.objects.filter(guest=guest).select_related("studio")
        return Response(GuestStudioSerializer(studios, many=True).data)

    def post(self, request: Request, guest_id) -> Response:
        guest = Guest.objects.get(pk=guest_id)
        input_serializer = GuestStudioInputSerializer(data=request.data)
        input_serializer.is_valid(raise_exception=True)
        try:
            guest_studio = GuestStudioService.add(
                guest=guest,
                actor=request.user,
                **input_serializer.validated_data,
            )
        except ValueError as error:
            return Response({"detail": str(error)}, status=status.HTTP_409_CONFLICT)
        return Response(
            GuestStudioSerializer(guest_studio).data, status=status.HTTP_201_CREATED
        )
