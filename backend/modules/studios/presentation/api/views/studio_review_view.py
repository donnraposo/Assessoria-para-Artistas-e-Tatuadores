from rest_framework import status
from rest_framework.request import Request
from rest_framework.response import Response
from rest_framework.views import APIView

from modules.identity.presentation.api.permissions import HasAdvisoryRole
from modules.studios.application.services import StudioReviewService
from modules.studios.infrastructure.persistence.models import Studio

from ..serializers import StudioSerializer


class StudioReviewView(APIView):
    permission_classes = [HasAdvisoryRole]

    def post(self, request: Request, studio_id) -> Response:
        studio = Studio.objects.get(pk=studio_id)
        try:
            StudioReviewService.review(
                studio,
                request.user,
                bool(request.data.get("approved")),
                str(request.data.get("reason", "")),
            )
        except ValueError as error:
            return Response({"detail": str(error)}, status=status.HTTP_409_CONFLICT)
        return Response(StudioSerializer(studio).data)
