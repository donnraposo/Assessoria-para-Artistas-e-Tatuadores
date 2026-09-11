from urllib.parse import parse_qs, urlparse

import pytest
from django.core import mail
from django.test import override_settings
from django.urls import reverse
from rest_framework.test import APIClient

from modules.identity.infrastructure.persistence.models import User


@pytest.mark.django_db
@override_settings(EMAIL_BACKEND="django.core.mail.backends.locmem.EmailBackend")
def test_password_reset_changes_password() -> None:
    user = User.objects.create_user(
        email="artist@example.com",
        password="old-strong-password",
        full_name="Artist",
    )
    client = APIClient()

    response = client.post(reverse("password-reset-request"), {"email": user.email}, format="json")
    query = parse_qs(urlparse(mail.outbox[0].body.split()[-1]).query)
    confirm = client.post(
        reverse("password-reset-confirm"),
        {"uid": query["uid"][0], "token": query["token"][0], "password": "new-strong-password"},
        format="json",
    )

    user.refresh_from_db()
    assert response.status_code == 200
    assert confirm.status_code == 200
    assert user.check_password("new-strong-password")


@pytest.mark.django_db
@override_settings(EMAIL_BACKEND="django.core.mail.backends.locmem.EmailBackend")
def test_password_reset_does_not_reveal_unknown_email() -> None:
    response = APIClient().post(
        reverse("password-reset-request"),
        {"email": "unknown@example.com"},
        format="json",
    )

    assert response.status_code == 200
    assert mail.outbox == []
