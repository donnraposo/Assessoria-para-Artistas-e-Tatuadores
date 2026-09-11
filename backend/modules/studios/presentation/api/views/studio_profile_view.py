from rest_framework.request import Request
from rest_framework.response import Response
from rest_framework.views import APIView

from modules.identity.presentation.api.permissions import HasStudioRole
from modules.studios.infrastructure.persistence.models import Studio

from ..serializers import StudioSerializer


class StudioProfileView(APIView):
    permission_classes = [HasStudioRole]

    def get(self, request: Request) -> Response:
        return Response(StudioSerializer(Studio.objects.get(owner=request.user)).data)

    def put(self, request: Request) -> Response:
        studio, _ = Studio.objects.get_or_create(owner=request.user)
        serializer = StudioSerializer(studio, data=request.data)
        serializer.is_valid(raise_exception=True)
        serializer.save()
        return Response(serializer.data)
