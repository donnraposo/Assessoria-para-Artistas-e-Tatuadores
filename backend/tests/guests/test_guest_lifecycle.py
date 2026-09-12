from datetime import date, timedelta
from decimal import Decimal

import pytest
from rest_framework.test import APIClient

from modules.artists.infrastructure.persistence.models import ArtistProfile
from modules.audit.infrastructure.persistence.models import AuditEvent
from modules.guests.application.services import (
    GuestProposalService,
    GuestStudioService,
    GuestTransitionService,
    ProposalTransitionService,
)
from modules.guests.domain.enums import GuestStatus, ProposalStatus
from modules.guests.infrastructure.persistence.models import GuestProposal, GuestStudio
from modules.identity.domain.enums import RoleType
from modules.identity.infrastructure.persistence.models import Role, User, UserRole
from modules.studios.domain.enums import StudioStatus
from modules.studios.infrastructure.persistence.models import Studio


def _build_proposal(**overrides) -> GuestProposal:
    artist_user = User.objects.create_user(
        email=overrides.pop("artist_email", "artist@example.com"), full_name="Artist"
    )
    studio_user = User.objects.create_user(
        email=overrides.pop("studio_email", "studio@example.com"), full_name="Studio"
    )
    artist = ArtistProfile.objects.create(
        user=artist_user,
        professional_name="Ink",
        styles=["blackwork"],
        minimum_tattoo_value=Decimal("500"),
        expected_ticket=Decimal("900"),
    )
    studio = Studio.objects.create(
        owner=studio_user,
        name="Black Room",
        country_code="BR",
        city="São Paulo",
        address="Rua Central, 1",
        status=StudioStatus.APPROVED,
    )
    defaults = {
        "artist": artist,
        "primary_studio": studio,
        "city": "Lisboa",
        "country_code": "PT",
        "starts_on": date.today() + timedelta(days=30),
        "ends_on": date.today() + timedelta(days=40),
        "timezone": "Europe/Lisbon",
        "currency": "EUR",
        "ads_budget": Decimal("1500"),
        "minimum_tattoo_value": Decimal("500"),
        "expected_ticket": Decimal("900"),
    }
    defaults.update(overrides)
    return GuestProposal.objects.create(**defaults)


@pytest.mark.django_db
def test_ready_proposal_creates_guest_snapshot_and_primary_studio() -> None:
    artist_user = User.objects.create_user(email="artist@example.com", full_name="Artist")
    studio_user = User.objects.create_user(email="studio@example.com", full_name="Studio")
    advisory = User.objects.create_user(email="admin@example.com", full_name="Admin")
    artist = ArtistProfile.objects.create(
        user=artist_user,
        professional_name="Ink",
        styles=["blackwork"],
        minimum_tattoo_value=Decimal("500"),
        expected_ticket=Decimal("900"),
    )
    studio = Studio.objects.create(
        owner=studio_user,
        name="Black Room",
        country_code="BR",
        city="São Paulo",
        address="Rua Central, 1",
        status=StudioStatus.APPROVED,
    )
    proposal = GuestProposal.objects.create(
        artist=artist,
        primary_studio=studio,
        city="Lisboa",
        country_code="PT",
        starts_on=date.today() + timedelta(days=30),
        ends_on=date.today() + timedelta(days=40),
        timezone="Europe/Lisbon",
        currency="EUR",
        ads_budget=Decimal("1500"),
        minimum_tattoo_value=Decimal("500"),
        expected_ticket=Decimal("900"),
    )

    GuestProposalService.mark_ready(proposal)
    guest = GuestProposalService.confirm(proposal, advisory)

    assert proposal.status == ProposalStatus.READY
    proposal.refresh_from_db()
    assert proposal.status == ProposalStatus.CONFIRMED
    assert guest.status == GuestStatus.CAPTURING
    assert GuestStudio.objects.filter(guest=guest, studio=studio).exists()
    assert AuditEvent.objects.filter(resource_id=str(guest.id)).exists()
    with pytest.raises(ValueError, match="reason"):
        GuestTransitionService.transition(guest, GuestStatus.CANCELLED, guest.artist.user)


@pytest.mark.django_db
def test_draft_proposal_can_be_declined_with_reason() -> None:
    advisory = User.objects.create_user(email="admin@example.com", full_name="Admin")
    proposal = _build_proposal()

    proposal = ProposalTransitionService.transition(
        proposal, ProposalStatus.DECLINED, advisory, "Client gave up on the trip"
    )

    assert proposal.status == ProposalStatus.DECLINED
    assert AuditEvent.objects.filter(
        resource_id=str(proposal.id), action="guest_proposal.status_changed"
    ).exists()


@pytest.mark.django_db
def test_proposal_transition_requires_reason() -> None:
    advisory = User.objects.create_user(email="admin@example.com", full_name="Admin")
    proposal = _build_proposal()

    with pytest.raises(ValueError, match="reason"):
        ProposalTransitionService.transition(proposal, ProposalStatus.CANCELLED, advisory, "")


@pytest.mark.django_db
def test_confirmed_proposal_cannot_be_declined() -> None:
    advisory = User.objects.create_user(email="admin@example.com", full_name="Admin")
    proposal = _build_proposal()
    GuestProposalService.mark_ready(proposal)
    GuestProposalService.confirm(proposal, advisory)

    with pytest.raises(ValueError, match="Invalid Proposal status transition"):
        ProposalTransitionService.transition(
            proposal, ProposalStatus.DECLINED, advisory, "Too late"
        )


@pytest.mark.django_db
def test_advisory_can_cancel_proposal_via_api() -> None:
    advisory_user = User.objects.create_user(email="admin@example.com", full_name="Admin")
    advisory_role = Role.objects.create(code=RoleType.ADVISORY, name="Advisory")
    UserRole.objects.create(user=advisory_user, role=advisory_role)
    proposal = _build_proposal()
    client = APIClient()
    client.force_authenticate(advisory_user)

    response = client.post(
        f"/api/v1/guests/proposals/{proposal.id}/transition/",
        {"status": ProposalStatus.CANCELLED, "reason": "Budget was withdrawn"},
        format="json",
    )

    assert response.status_code == 200
    assert response.json()["status"] == ProposalStatus.CANCELLED


@pytest.mark.django_db
def test_advisory_can_add_second_studio_to_confirmed_guest() -> None:
    advisory_user = User.objects.create_user(email="admin@example.com", full_name="Admin")
    advisory_role = Role.objects.create(code=RoleType.ADVISORY, name="Advisory")
    UserRole.objects.create(user=advisory_user, role=advisory_role)
    second_studio_owner = User.objects.create_user(
        email="studio2@example.com", full_name="Second Studio Owner"
    )
    second_studio = Studio.objects.create(
        owner=second_studio_owner,
        name="Second Room",
        country_code="PT",
        city="Lisboa",
        address="Rua Nova, 2",
        status=StudioStatus.APPROVED,
    )
    proposal = _build_proposal()
    GuestProposalService.mark_ready(proposal)
    guest = GuestProposalService.confirm(proposal, advisory_user)
    client = APIClient()
    client.force_authenticate(advisory_user)

    non_overlapping_start = guest.studios.first().ends_at + timedelta(hours=1)
    response = client.post(
        f"/api/v1/guests/{guest.id}/studios/",
        {
            "studio": str(second_studio.id),
            "starts_at": non_overlapping_start.isoformat(),
            "ends_at": (non_overlapping_start + timedelta(hours=4)).isoformat(),
        },
        format="json",
    )

    assert response.status_code == 201
    assert GuestStudio.objects.filter(guest=guest, studio=second_studio).exists()


@pytest.mark.django_db
def test_overlapping_studio_period_is_rejected() -> None:
    advisory_user = User.objects.create_user(email="admin@example.com", full_name="Admin")
    second_studio_owner = User.objects.create_user(
        email="studio2@example.com", full_name="Second Studio Owner"
    )
    second_studio = Studio.objects.create(
        owner=second_studio_owner,
        name="Second Room",
        country_code="PT",
        city="Lisboa",
        address="Rua Nova, 2",
        status=StudioStatus.APPROVED,
    )
    proposal = _build_proposal()
    GuestProposalService.mark_ready(proposal)
    guest = GuestProposalService.confirm(proposal, advisory_user)
    primary = guest.studios.first()

    with pytest.raises(ValueError, match="overlaps"):
        GuestStudioService.add(
            guest=guest,
            studio=second_studio,
            actor=advisory_user,
            starts_at=primary.starts_at,
            ends_at=primary.starts_at + timedelta(hours=1),
        )
