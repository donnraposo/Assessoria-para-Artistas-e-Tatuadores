from django.conf import settings
from django.core.mail import send_mail
from django.db import transaction
from django.utils import timezone

from modules.notifications.domain.enums import NotificationStatus
from modules.notifications.infrastructure.persistence.models import Notification


class NotificationService:
    max_attempts = 3

    @staticmethod
    def enqueue(*, recipient, category: str, subject: str, message: str, key: str) -> Notification:
        notification, _ = Notification.objects.get_or_create(
            idempotency_key=key,
            defaults={
                "recipient": recipient,
                "category": category,
                "subject": subject,
                "message": message,
            },
        )
        return notification

    @classmethod
    @transaction.atomic
    def deliver(cls, notification: Notification) -> Notification:
        locked = Notification.objects.select_for_update().get(pk=notification.pk)
        if locked.status == NotificationStatus.SENT or locked.attempts >= cls.max_attempts:
            return locked
        locked.attempts += 1
        try:
            send_mail(
                locked.subject,
                locked.message,
                settings.DEFAULT_FROM_EMAIL,
                [locked.recipient.email],
                fail_silently=False,
            )
        except Exception as error:
            locked.status = NotificationStatus.FAILED
            locked.last_error = str(error)[:2000]
            locked.save(update_fields=["attempts", "status", "last_error"])
            return locked
        locked.status = NotificationStatus.SENT
        locked.sent_at = timezone.now()
        locked.last_error = ""
        locked.save(update_fields=["attempts", "status", "sent_at", "last_error"])
        return locked
