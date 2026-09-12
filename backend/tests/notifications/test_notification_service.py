import pytest
from django.core import mail
from django.test import override_settings

from modules.identity.infrastructure.persistence.models import User
from modules.notifications.application.services import NotificationService
from modules.notifications.domain.enums import NotificationStatus


@pytest.mark.django_db
@override_settings(EMAIL_BACKEND="django.core.mail.backends.locmem.EmailBackend")
def test_notification_delivery_is_idempotent() -> None:
    user = User.objects.create_user(email="recipient@example.com", full_name="Recipient")
    first = NotificationService.enqueue(
        recipient=user,
        category="test",
        subject="Operational update",
        message="Your operation was updated.",
        key="test-notification-001",
    )
    repeated = NotificationService.enqueue(
        recipient=user,
        category="test",
        subject="Operational update",
        message="Your operation was updated.",
        key="test-notification-001",
    )

    delivered = NotificationService.deliver(first)
    NotificationService.deliver(first)

    assert repeated.id == first.id
    assert delivered.status == NotificationStatus.SENT
    assert delivered.attempts == 1
    assert len(mail.outbox) == 1
