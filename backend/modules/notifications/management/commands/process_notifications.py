from django.core.management.base import BaseCommand

from modules.notifications.application.services import NotificationService
from modules.notifications.domain.enums import NotificationStatus
from modules.notifications.infrastructure.persistence.models import Notification


class Command(BaseCommand):
    help = "Deliver pending or retryable email notifications."

    def handle(self, *args, **options):
        notifications = Notification.objects.filter(
            status__in=[NotificationStatus.PENDING, NotificationStatus.FAILED],
            attempts__lt=NotificationService.max_attempts,
        ).order_by("created_at")[:100]
        delivered = 0
        for notification in notifications:
            result = NotificationService.deliver(notification)
            delivered += result.status == NotificationStatus.SENT
        self.stdout.write(self.style.SUCCESS(f"Delivered {delivered} notification(s)."))
