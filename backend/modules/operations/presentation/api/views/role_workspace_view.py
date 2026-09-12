from rest_framework import status
from rest_framework.request import Request
from rest_framework.response import Response
from rest_framework.views import APIView

from modules.operations.application.services import RoleWorkspaceService


class RoleWorkspaceView(APIView):
    def get(self, request: Request) -> Response:
        try:
            workspace = RoleWorkspaceService.build(request.user)
        except ValueError as error:
            return Response({"detail": str(error)}, status=status.HTTP_403_FORBIDDEN)
        return Response(workspace)

