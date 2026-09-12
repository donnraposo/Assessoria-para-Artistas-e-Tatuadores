from django.shortcuts import get_object_or_404
from django.utils import timezone
from rest_framework.request import Request
from rest_framework.response import Response
from rest_framework.views import APIView

from modules.notifications.infrastructure.persistence.models import Notification
from modules.notifications.presentation.api.serializers import NotificationSerializer


class NotificationReadView(APIView):
    def post(self, request: Request, notification_id) -> Response:
        notification = get_object_or_404(
            Notification,
            pk=notification_id,
            recipient=request.user,
        )
        if notification.read_at is None:
            notification.read_at = timezone.now()
            notification.save(update_fields=["read_at"])
        return Response(NotificationSerializer(notification).data)
