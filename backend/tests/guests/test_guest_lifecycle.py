from datetime import date, timedelta
from decimal import Decimal

import pytest

from modules.artists.domain.enums import ApplicationStatus
from modules.artists.infrastructure.persistence.models import ArtistApplication, ArtistProfile
from modules.audit.infrastructure.persistence.models import AuditEvent
from modules.guests.application.services import GuestProposalService, GuestTransitionService
from modules.guests.domain.enums import GuestStatus, ProposalStatus
from modules.guests.infrastructure.persistence.models import GuestProposal, GuestStudio
from modules.identity.infrastructure.persistence.models import User
from modules.studios.domain.enums import StudioStatus
from modules.studios.infrastructure.persistence.models import Studio


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
    ArtistApplication.objects.create(artist=artist, status=ApplicationStatus.APPROVED)
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
