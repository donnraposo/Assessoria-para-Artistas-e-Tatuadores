from rest_framework.request import Request
from rest_framework.response import Response
from rest_framework.views import APIView

from modules.identity.presentation.api.permissions import HasStudioRole
from modules.studios.infrastructure.persistence.models import Studio

from ..serializers import StudioAvailabilitySerializer


class StudioAvailabilityCollectionView(APIView):
    permission_classes = [HasStudioRole]

    def get(self, request: Request) -> Response:
        studio = Studio.objects.get(owner=request.user)
        return Response(StudioAvailabilitySerializer(studio.availability.all(), many=True).data)

    def post(self, request: Request) -> Response:
        studio = Studio.objects.get(owner=request.user)
        serializer = StudioAvailabilitySerializer(data=request.data, context={"studio": studio})
        serializer.is_valid(raise_exception=True)
        serializer.save(studio=studio)
        return Response(serializer.data, status=201)
