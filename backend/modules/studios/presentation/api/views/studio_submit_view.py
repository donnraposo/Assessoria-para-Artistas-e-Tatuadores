from rest_framework import status
from rest_framework.request import Request
from rest_framework.response import Response
from rest_framework.views import APIView

from modules.identity.presentation.api.permissions import HasStudioRole
from modules.studios.application.services import StudioReviewService
from modules.studios.infrastructure.persistence.models import Studio

from ..serializers import StudioSerializer


class StudioSubmitView(APIView):
    permission_classes = [HasStudioRole]

    def post(self, request: Request) -> Response:
        studio = Studio.objects.get(owner=request.user)
        try:
            StudioReviewService.submit(studio)
        except ValueError as error:
            return Response({"detail": str(error)}, status=status.HTTP_409_CONFLICT)
        return Response(StudioSerializer(studio).data)
