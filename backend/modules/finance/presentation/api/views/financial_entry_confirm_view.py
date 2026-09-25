from rest_framework import status
from rest_framework.request import Request
from rest_framework.response import Response
from rest_framework.views import APIView

from modules.finance.application.services import FinancialEntryService
from modules.finance.infrastructure.persistence.models import FinancialEntry
from modules.identity.presentation.api.permissions import HasAdvisoryRole

from ..serializers import FinancialEntrySerializer


class FinancialEntryConfirmView(APIView):
    permission_classes = [HasAdvisoryRole]

    def post(self, request: Request, entry_id) -> Response:
        entry = FinancialEntry.objects.get(pk=entry_id)
        try:
            entry = FinancialEntryService.confirm(
                entry,
                request.user,
                str(request.data.get("reference", "")),
            )
        except ValueError as error:
            return Response({"detail": str(error)}, status=status.HTTP_409_CONFLICT)
        return Response(FinancialEntrySerializer(entry).data)
