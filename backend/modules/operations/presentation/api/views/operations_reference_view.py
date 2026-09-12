from rest_framework.request import Request
from rest_framework.response import Response
from rest_framework.views import APIView

from modules.identity.presentation.api.permissions import HasAdvisoryRole
from modules.operations.application.services import OperationsReferenceService


class OperationsReferenceView(APIView):
    permission_classes = [HasAdvisoryRole]

    def get(self, request: Request) -> Response:
        return Response(OperationsReferenceService.build())
