from django.contrib.auth import logout
from rest_framework.request import Request
from rest_framework.response import Response
from rest_framework.views import APIView


class LogoutView(APIView):
    def post(self, request: Request) -> Response:
        logout(request)
        return Response(status=204)
