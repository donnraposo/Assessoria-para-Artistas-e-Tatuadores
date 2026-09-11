from rest_framework import status
from rest_framework.permissions import AllowAny
from rest_framework.request import Request
from rest_framework.response import Response
from rest_framework.views import APIView

from modules.identity.application.services import PasswordResetService

from ..serializers import PasswordResetConfirmSerializer
from ..throttles import PasswordResetRateThrottle


class PasswordResetConfirmView(APIView):
    authentication_classes = []
    permission_classes = [AllowAny]
    throttle_classes = [PasswordResetRateThrottle]

    def post(self, request: Request) -> Response:
        serializer = PasswordResetConfirmSerializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        changed = PasswordResetService.confirm(**serializer.validated_data)
        if not changed:
            return Response(
                {"detail": "Invalid or expired link."},
                status=status.HTTP_400_BAD_REQUEST,
            )
        return Response({"detail": "Password reset successfully."})
