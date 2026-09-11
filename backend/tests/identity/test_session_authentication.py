import pytest
from django.urls import reverse
from rest_framework.test import APIClient

from modules.identity.infrastructure.persistence.models import User


@pytest.mark.django_db
def test_login_me_and_logout_flow() -> None:
    User.objects.create_user(email="artist@example.com", password="strong-pass", full_name="Artist")
    client = APIClient()

    login_response = client.post(
        reverse("login"),
        {"email": "ARTIST@example.com", "password": "strong-pass"},
        format="json",
    )
    me_response = client.get(reverse("current-user"))
    logout_response = client.post(reverse("logout"))
    unauthorized_response = client.get(reverse("current-user"))

    assert login_response.status_code == 200
    assert me_response.status_code == 200
    assert me_response.json()["email"] == "artist@example.com"
    assert logout_response.status_code == 204
    assert unauthorized_response.status_code == 403


@pytest.mark.django_db
def test_login_rejects_invalid_credentials() -> None:
    client = APIClient()

    response = client.post(
        reverse("login"),
        {"email": "unknown@example.com", "password": "invalid"},
        format="json",
    )

    assert response.status_code == 403
