from rest_framework import status
from rest_framework.request import Request
from rest_framework.response import Response
from rest_framework.views import APIView

from modules.artists.application.services import ArtistApplicationService
from modules.artists.infrastructure.persistence.models import ArtistApplication
from modules.identity.presentation.api.permissions import HasAdvisoryRole

from ..serializers import ArtistApplicationSerializer


class ArtistApplicationReviewView(APIView):
    permission_classes = [HasAdvisoryRole]

    def post(self, request: Request, application_id) -> Response:
        application = ArtistApplication.objects.get(pk=application_id)
        try:
            ArtistApplicationService.review(
                application,
                request.user,
                bool(request.data.get("approved")),
                str(request.data.get("reason", "")),
            )
        except ValueError as error:
            return Response({"detail": str(error)}, status=status.HTTP_409_CONFLICT)
        return Response(ArtistApplicationSerializer(application).data)
