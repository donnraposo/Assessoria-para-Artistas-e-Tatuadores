from django.shortcuts import get_object_or_404
from rest_framework import status
from rest_framework.request import Request
from rest_framework.response import Response
from rest_framework.views import APIView

from modules.identity.presentation.api.permissions import HasAdvisoryRole
from modules.logistics.infrastructure.persistence.models import TravelSegment
from modules.logistics.presentation.api.serializers import TravelSegmentSerializer


class TravelSegmentDetailView(APIView):
    permission_classes = [HasAdvisoryRole]

    def patch(self, request: Request, segment_id) -> Response:
        segment = get_object_or_404(TravelSegment, pk=segment_id)
        serializer = TravelSegmentSerializer(
            segment,
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
