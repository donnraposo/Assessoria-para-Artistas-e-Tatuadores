from rest_framework.request import Request
from rest_framework.response import Response
from rest_framework.views import APIView

from modules.notifications.infrastructure.persistence.models import Notification
from modules.notifications.presentation.api.serializers import NotificationSerializer


class NotificationCollectionView(APIView):
    def get(self, request: Request) -> Response:
        notifications = Notification.objects.filter(recipient=request.user)[:50]
        return Response(NotificationSerializer(notifications, many=True).data)
