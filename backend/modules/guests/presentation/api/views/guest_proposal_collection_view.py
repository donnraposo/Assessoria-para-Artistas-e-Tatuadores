from rest_framework.request import Request
from rest_framework.response import Response
from rest_framework.views import APIView

from modules.guests.infrastructure.persistence.models import GuestProposal
from modules.identity.presentation.api.permissions import HasAdvisoryRole

from ..serializers import GuestProposalSerializer


class GuestProposalCollectionView(APIView):
    permission_classes = [HasAdvisoryRole]

    def get(self, request: Request) -> Response:
        proposals = GuestProposal.objects.select_related("artist", "primary_studio")
        return Response(GuestProposalSerializer(proposals, many=True).data)

    def post(self, request: Request) -> Response:
        serializer = GuestProposalSerializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        serializer.save()
        return Response(serializer.data, status=201)
