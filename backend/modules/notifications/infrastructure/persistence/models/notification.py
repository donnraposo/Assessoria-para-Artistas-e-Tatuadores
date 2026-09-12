import uuid

from django.conf import settings
from django.db import models

from modules.notifications.domain.enums import NotificationStatus


class Notification(models.Model):
    id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)
    recipient = models.ForeignKey(
        settings.AUTH_USER_MODEL,
        on_delete=models.PROTECT,
        related_name="notifications",
    )
    category = models.CharField(max_length=80)
    subject = models.CharField(max_length=180)
    message = models.TextField()
    idempotency_key = models.CharField(max_length=160, unique=True)
    status = models.CharField(
        max_length=12,
        choices=NotificationStatus.choices,
        default=NotificationStatus.PENDING,
    )
    attempts = models.PositiveSmallIntegerField(default=0)
    last_error = models.TextField(blank=True)
    created_at = models.DateTimeField(auto_now_add=True)
    sent_at = models.DateTimeField(null=True, blank=True)
    read_at = models.DateTimeField(null=True, blank=True)

    class Meta:
        db_table = "notifications_notification"
        ordering = ["-created_at"]

    def __str__(self) -> str:
        return f"{self.category}:{self.recipient_id}:{self.status}"
