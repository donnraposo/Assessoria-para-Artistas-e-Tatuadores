from rest_framework.request import Request
from rest_framework.response import Response
from rest_framework.views import APIView

from modules.identity.presentation.api.permissions import HasAdvisoryRole

from ..serializers import BookingRequestSerializer


class BookingRequestCreateView(APIView):
    permission_classes = [HasAdvisoryRole]

    def post(self, request: Request) -> Response:
        serializer = BookingRequestSerializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        serializer.save(requested_by=request.user)
        return Response(serializer.data, status=201)
