from rest_framework import serializers

from modules.notifications.infrastructure.persistence.models import Notification


class NotificationSerializer(serializers.ModelSerializer):
    class Meta:
        model = Notification
        fields = ["id", "category", "subject", "message", "status", "created_at", "read_at"]
        read_only_fields = fields
