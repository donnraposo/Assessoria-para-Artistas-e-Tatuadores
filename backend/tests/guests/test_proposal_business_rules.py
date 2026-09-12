from datetime import date, timedelta
from decimal import Decimal

import pytest

from modules.artists.domain.enums import ApplicationStatus
from modules.artists.infrastructure.persistence.models import ArtistApplication, ArtistProfile
from modules.guests.application.services import GuestProposalService
from modules.guests.infrastructure.persistence.models import GuestProposal
from modules.identity.infrastructure.persistence.models import User
from modules.studios.domain.enums import StudioStatus
from modules.studios.infrastructure.persistence.models import Studio


def build_proposal(
    suffix: str,
    *,
    application_status: str | None = ApplicationStatus.APPROVED,
    artist_minimum: Decimal = Decimal("500"),
    proposal_minimum: Decimal = Decimal("500"),
) -> GuestProposal:
    artist_user = User.objects.create_user(
        email=f"artist-{suffix}@example.com",
        full_name="Ana Ink",
    )
    studio_user = User.objects.create_user(
        email=f"studio-{suffix}@example.com",
        full_name="Studio Owner",
    )
    artist = ArtistProfile.objects.create(
        user=artist_user,
        professional_name="Ana Ink",
        styles=["blackwork"],
        minimum_tattoo_value=artist_minimum,
        expected_ticket=Decimal("900"),
    )
    if application_status is not None:
        ArtistApplication.objects.create(artist=artist, status=application_status)
    studio = Studio.objects.create(
        owner=studio_user,
        name="Black Room",
        country_code="BR",
        city="São Paulo",
        address="Rua Central, 1",
        status=StudioStatus.APPROVED,
    )
    return GuestProposal.objects.create(
        artist=artist,
        primary_studio=studio,
        city="Lisboa",
        country_code="PT",
        starts_on=date.today() + timedelta(days=30),
        ends_on=date.today() + timedelta(days=40),
        timezone="Europe/Lisbon",
        currency="EUR",
        ads_budget=Decimal("1500"),
        minimum_tattoo_value=proposal_minimum,
        expected_ticket=Decimal("900"),
    )


@pytest.mark.django_db
def test_proposal_requires_an_approved_artist_application() -> None:
    proposal = build_proposal("under-review", application_status=ApplicationStatus.UNDER_REVIEW)

    with pytest.raises(ValueError, match="Artist application must be approved"):
        GuestProposalService.mark_ready(proposal)


@pytest.mark.django_db
def test_rejected_artist_cannot_reach_a_ready_proposal() -> None:
    proposal = build_proposal("rejected", application_status=ApplicationStatus.REJECTED)

    with pytest.raises(ValueError, match="Artist application must be approved"):
        GuestProposalService.mark_ready(proposal)


@pytest.mark.django_db
def test_artist_without_any_application_cannot_reach_a_ready_proposal() -> None:
    proposal = build_proposal("absent", application_status=None)

    with pytest.raises(ValueError, match="Artist application must be approved"):
        GuestProposalService.mark_ready(proposal)


@pytest.mark.django_db
def test_proposal_minimum_cannot_undercut_the_value_declared_by_the_artist() -> None:
    proposal = build_proposal(
        "floor",
        artist_minimum=Decimal("500"),
        proposal_minimum=Decimal("400"),
    )

    with pytest.raises(ValueError, match="below the minimum declared by the Artist"):
        GuestProposalService.mark_ready(proposal)


@pytest.mark.django_db
def test_proposal_minimum_may_exceed_the_value_declared_by_the_artist() -> None:
    proposal = build_proposal(
        "above-floor",
        artist_minimum=Decimal("500"),
        proposal_minimum=Decimal("700"),
    )

    GuestProposalService.mark_ready(proposal)

    assert proposal.status == "READY"


@pytest.mark.django_db
def test_floor_is_checked_against_the_current_artist_profile() -> None:
    proposal = build_proposal("raised-floor")
    artist = proposal.artist
    artist.minimum_tattoo_value = Decimal("900")
    artist.save(update_fields=["minimum_tattoo_value", "updated_at"])

    with pytest.raises(ValueError, match="below the minimum declared by the Artist"):
        GuestProposalService.mark_ready(proposal)
