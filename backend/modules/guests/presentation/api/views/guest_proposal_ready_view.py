from rest_framework import status
from rest_framework.request import Request
from rest_framework.response import Response
from rest_framework.views import APIView

from modules.guests.application.services import GuestProposalService
from modules.guests.infrastructure.persistence.models import GuestProposal
from modules.identity.presentation.api.permissions import HasAdvisoryRole

from ..serializers import GuestProposalSerializer


class GuestProposalReadyView(APIView):
    permission_classes = [HasAdvisoryRole]

    def post(self, request: Request, proposal_id) -> Response:
        proposal = GuestProposal.objects.get(pk=proposal_id)
        try:
            GuestProposalService.mark_ready(proposal)
        except ValueError as error:
            return Response({"detail": str(error)}, status=status.HTTP_409_CONFLICT)
        return Response(GuestProposalSerializer(proposal).data)
