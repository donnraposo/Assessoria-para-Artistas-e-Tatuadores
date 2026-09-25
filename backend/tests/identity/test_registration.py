import pytest
from django.urls import reverse
from rest_framework.test import APIClient

from modules.audit.infrastructure.persistence.models import AuditEvent
from modules.identity.domain.enums import RoleType
from modules.identity.infrastructure.persistence.models import User


@pytest.mark.django_db
def test_artist_can_self_register_and_is_logged_in() -> None:
    client = APIClient()

    response = client.post(
        reverse("register"),
        {
            "email": "new.artist@example.com",
            "password": "correct horse battery staple",
            "full_name": "New Artist",
            "role": RoleType.ARTIST,
        },
        format="json",
    )
    me_response = client.get(reverse("current-user"))

    assert response.status_code == 201
    user = User.objects.get(email="new.artist@example.com")
    assert user.roles.filter(role__code=RoleType.ARTIST).exists()
    assert me_response.status_code == 200
    assert AuditEvent.objects.filter(
        action="user.registered", resource_id=str(user.id)
    ).exists()


@pytest.mark.django_db
def test_studio_can_self_register() -> None:
    client = APIClient()

    response = client.post(
        reverse("register"),
        {
            "email": "new.studio@example.com",
            "password": "correct horse battery staple",
            "full_name": "New Studio",
            "role": RoleType.STUDIO,
        },
        format="json",
    )

    assert response.status_code == 201
    user = User.objects.get(email="new.studio@example.com")
    assert user.roles.filter(role__code=RoleType.STUDIO).exists()


@pytest.mark.django_db
def test_registration_rejects_advisory_role() -> None:
    response = APIClient().post(
        reverse("register"),
        {
            "email": "wannabe.admin@example.com",
            "password": "correct horse battery staple",
            "full_name": "Wannabe Admin",
            "role": RoleType.ADVISORY,
        },
        format="json",
    )

    assert response.status_code == 400
    assert not User.objects.filter(email="wannabe.admin@example.com").exists()


@pytest.mark.django_db
def test_registration_rejects_duplicate_email() -> None:
    User.objects.create_user(
        email="existing@example.com", password="strong-pass", full_name="Existing"
    )

    response = APIClient().post(
        reverse("register"),
        {
            "email": "existing@example.com",
            "password": "correct horse battery staple",
            "full_name": "Duplicate",
            "role": RoleType.ARTIST,
        },
        format="json",
    )

    assert response.status_code == 400


@pytest.mark.django_db
def test_registration_rejects_weak_password() -> None:
    response = APIClient().post(
        reverse("register"),
        {
            "email": "weak.password@example.com",
            "password": "1234",
            "full_name": "Weak Password",
            "role": RoleType.ARTIST,
        },
        format="json",
    )

    assert response.status_code == 400
    assert not User.objects.filter(email="weak.password@example.com").exists()
