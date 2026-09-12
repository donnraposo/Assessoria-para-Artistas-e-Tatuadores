from datetime import UTC, datetime, timedelta
from decimal import Decimal

import pytest
from rest_framework.test import APIClient

from modules.identity.domain.enums import RoleType
from modules.identity.infrastructure.persistence.models import Role, User, UserRole
from modules.studios.domain.enums import PricingType, StudioStatus
from modules.studios.infrastructure.persistence.models import (
    Studio,
    StudioAvailability,
    Workstation,
)


def _build_studio(email: str = "studio-offer@example.com") -> tuple[Studio, User]:
    owner = User.objects.create_user(email=email, full_name="Studio Owner")
    role, _ = Role.objects.get_or_create(code=RoleType.STUDIO, defaults={"name": "Studio"})
    UserRole.objects.create(user=owner, role=role)
    studio = Studio.objects.create(
        owner=owner,
        name="Black Room",
        country_code="BR",
        city="São Paulo",
        address="Rua Central, 1",
        status=StudioStatus.APPROVED,
    )
    return studio, owner


@pytest.mark.django_db
def test_studio_can_manage_own_workstations() -> None:
    studio, owner = _build_studio()
    client = APIClient()
    client.force_authenticate(owner)

    response = client.post(
        "/api/v1/studios/me/workstations/", {"name": "Station 1"}, format="json"
    )
    listing = client.get("/api/v1/studios/me/workstations/")

    assert response.status_code == 201
    assert Workstation.objects.filter(studio=studio, name="Station 1").exists()
    assert len(listing.json()) == 1


@pytest.mark.django_db
def test_studio_can_register_pricing() -> None:
    studio, owner = _build_studio()
    client = APIClient()
    client.force_authenticate(owner)

    response = client.post(
        "/api/v1/studios/me/prices/",
        {
            "pricing_type": PricingType.DAILY,
            "amount": "300.00",
            "currency": "BRL",
            "valid_from": "2026-01-01",
        },
        format="json",
    )

    assert response.status_code == 201
    assert studio.prices.filter(pricing_type=PricingType.DAILY, amount=Decimal("300.00")).exists()


@pytest.mark.django_db
def test_pricing_validity_end_cannot_precede_start() -> None:
    _, owner = _build_studio()
    client = APIClient()
    client.force_authenticate(owner)

    response = client.post(
        "/api/v1/studios/me/prices/",
        {
            "pricing_type": PricingType.DAILY,
            "amount": "300.00",
            "currency": "BRL",
            "valid_from": "2026-01-10",
            "valid_until": "2026-01-01",
        },
        format="json",
    )

    assert response.status_code == 400


@pytest.mark.django_db
def test_studio_can_register_availability_with_workstation() -> None:
    studio, owner = _build_studio()
    workstation = Workstation.objects.create(studio=studio, name="Station 1")
    start = datetime.now(UTC) + timedelta(days=5)
    client = APIClient()
    client.force_authenticate(owner)

    response = client.post(
        "/api/v1/studios/me/availability/",
        {
            "workstation": str(workstation.id),
            "starts_at": start.isoformat(),
            "ends_at": (start + timedelta(hours=8)).isoformat(),
            "capacity": 1,
            "timezone": "America/Sao_Paulo",
        },
        format="json",
    )

    assert response.status_code == 201
    assert StudioAvailability.objects.filter(studio=studio, workstation=workstation).exists()


@pytest.mark.django_db
def test_availability_rejects_workstation_from_another_studio() -> None:
    _, owner = _build_studio()
    other_studio, _ = _build_studio(email="studio-other@example.com")
    other_workstation = Workstation.objects.create(studio=other_studio, name="Other Station")
    start = datetime.now(UTC) + timedelta(days=5)
    client = APIClient()
    client.force_authenticate(owner)

    response = client.post(
        "/api/v1/studios/me/availability/",
        {
            "workstation": str(other_workstation.id),
            "starts_at": start.isoformat(),
            "ends_at": (start + timedelta(hours=8)).isoformat(),
            "capacity": 1,
            "timezone": "America/Sao_Paulo",
        },
        format="json",
    )

    assert response.status_code == 400
