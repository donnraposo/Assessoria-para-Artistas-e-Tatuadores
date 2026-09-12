from django.shortcuts import get_object_or_404
from rest_framework.request import Request
from rest_framework.response import Response
from rest_framework.views import APIView

from modules.artists.infrastructure.persistence.models import ArtistApplication
from modules.identity.presentation.api.permissions import HasAdvisoryRole

from ..serializers import ArtistApplicationDetailSerializer


class ArtistApplicationDetailView(APIView):
    permission_classes = [HasAdvisoryRole]

    def get(self, request: Request, application_id) -> Response:
        application = get_object_or_404(
            ArtistApplication.objects.select_related("artist", "artist__user"),
            pk=application_id,
        )
        return Response(ArtistApplicationDetailSerializer(application).data)
