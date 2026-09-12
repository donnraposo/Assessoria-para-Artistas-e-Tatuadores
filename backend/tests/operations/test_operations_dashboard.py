import pytest
from rest_framework.test import APIClient

from modules.finance.domain.enums import FinancialEntryStatus, FinancialEntryType
from modules.finance.infrastructure.persistence.models import FinancialEntry
from modules.identity.domain.enums import RoleType
from modules.identity.infrastructure.persistence.models import Role, User, UserRole
from tests.sales.test_closing import build_scenario


@pytest.mark.django_db
def test_advisory_dashboard_and_queue_are_paginated() -> None:
    _, advisory, _, _, _ = build_scenario("operations")
    role = Role.objects.create(code=RoleType.ADVISORY, name="Advisory")
    UserRole.objects.create(user=advisory, role=role)
    client = APIClient()
    client.force_authenticate(advisory)

    dashboard = client.get("/api/v1/operations/dashboard/")
    queue = client.get("/api/v1/operations/queues/open-leads/?page=1&page_size=1")

    assert dashboard.status_code == 200
    assert dashboard.data["queues"]["open_leads"] == 1
    assert queue.status_code == 200
    assert queue.data["count"] == 1
    assert len(queue.data["results"]) == 1


@pytest.mark.django_db
def test_artist_cannot_access_operations_dashboard() -> None:
    artist = User.objects.create_user(email="artist-dashboard@example.com", full_name="Artist")
    role = Role.objects.create(code=RoleType.ARTIST, name="Artist")
    UserRole.objects.create(user=artist, role=role)
    client = APIClient()
    client.force_authenticate(artist)

    response = client.get("/api/v1/operations/dashboard/")

    assert response.status_code == 403


@pytest.mark.django_db
def test_artist_workspace_contains_only_artist_operational_data() -> None:
    artist_user, _, guest, _, _ = build_scenario("artist-workspace")
    role = Role.objects.create(code=RoleType.ARTIST, name="Artist")
    UserRole.objects.create(user=artist_user, role=role)
    FinancialEntry.objects.create(
        guest=guest,
        entry_type=FinancialEntryType.ARTIST_RECEIVABLE,
        status=FinancialEntryStatus.EXPECTED,
        amount="720.00",
        currency="BRL",
        source_reference="artist-workspace-balance",
    )
    client = APIClient()
    client.force_authenticate(artist_user)

    response = client.get("/api/v1/operations/workspace/")

    assert response.status_code == 200
    assert response.data["role"] == RoleType.ARTIST
    assert response.data["balances"] == [{"currency": "BRL", "total": 720}]
    assert {card["key"] for card in response.data["cards"]} == {
        "active_guests",
        "upcoming_appointments",
        "pending_logistics",
        "notifications",
    }


@pytest.mark.django_db
def test_studio_workspace_does_not_expose_commercial_data() -> None:
    _, _, _, _, appointment = build_scenario("studio-workspace")
    studio_user = appointment.studio.owner
    role = Role.objects.create(code=RoleType.STUDIO, name="Studio")
    UserRole.objects.create(user=studio_user, role=role)
    client = APIClient()
    client.force_authenticate(studio_user)

    response = client.get("/api/v1/operations/workspace/")

    assert response.status_code == 200
    assert response.data["role"] == RoleType.STUDIO
    assert response.data["balances"] == []
    serialized = str(response.data).lower()
    assert "agency_revenue" not in serialized
    assert "artist_receivable" not in serialized
    assert "open_leads" not in serialized
