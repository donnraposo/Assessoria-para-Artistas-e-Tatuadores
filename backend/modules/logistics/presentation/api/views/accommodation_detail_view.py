from django.shortcuts import get_object_or_404
from rest_framework import status
from rest_framework.request import Request
from rest_framework.response import Response
from rest_framework.views import APIView

from modules.identity.presentation.api.permissions import HasAdvisoryRole
from modules.logistics.infrastructure.persistence.models import Accommodation
from modules.logistics.presentation.api.serializers import AccommodationSerializer


class AccommodationDetailView(APIView):
    permission_classes = [HasAdvisoryRole]

    def patch(self, request: Request, accommodation_id) -> Response:
        accommodation = get_object_or_404(Accommodation, pk=accommodation_id)
        serializer = AccommodationSerializer(
            accommodation,
            data=request.data,
            partial=True,
            context={"request": request},
        )
        serializer.is_valid(raise_exception=True)
        try:
            serializer.save()
        except ValueError as error:
            return Response({"detail": str(error)}, status=status.HTTP_409_CONFLICT)
        return Response(serializer.data)
