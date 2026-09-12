from rest_framework import status
from rest_framework.request import Request
from rest_framework.response import Response
from rest_framework.views import APIView

from modules.identity.presentation.api.permissions import HasAdvisoryRole
from modules.operations.application.services import OperationsQueueService


class OperationsQueueView(APIView):
    permission_classes = [HasAdvisoryRole]

    def get(self, request: Request, queue_name: str) -> Response:
        try:
            page_number = int(request.query_params.get("page", "1"))
            page_size = int(request.query_params.get("page_size", "20"))
            result = OperationsQueueService.get(queue_name, page_number, page_size)
        except (TypeError, ValueError) as error:
            return Response({"detail": str(error)}, status=status.HTTP_400_BAD_REQUEST)
        return Response(result)
