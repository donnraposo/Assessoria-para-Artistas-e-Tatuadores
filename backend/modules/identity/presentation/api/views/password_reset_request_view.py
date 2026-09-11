from rest_framework.permissions import AllowAny
from rest_framework.request import Request
from rest_framework.response import Response
from rest_framework.views import APIView

from modules.identity.application.services import PasswordResetService

from ..serializers import PasswordResetRequestSerializer
from ..throttles import PasswordResetRateThrottle


class PasswordResetRequestView(APIView):
    authentication_classes = []
    permission_classes = [AllowAny]
    throttle_classes = [PasswordResetRateThrottle]

    def post(self, request: Request) -> Response:
        serializer = PasswordResetRequestSerializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        PasswordResetService.request(serializer.validated_data["email"])
        return Response({"detail": "If the email exists, instructions will be sent."})
