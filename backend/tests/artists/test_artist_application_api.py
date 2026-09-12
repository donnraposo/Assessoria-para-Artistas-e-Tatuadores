from decimal import Decimal

import pytest
from rest_framework.test import APIClient

from modules.artists.domain.enums import ApplicationStatus
from modules.artists.infrastructure.persistence.models import (
    ArtistApplication,
    ArtistProfile,
    PortfolioItem,
)
from modules.identity.domain.enums import RoleType
from modules.identity.infrastructure.persistence.models import Role, User, UserRole


def build_artist(suffix: str) -> tuple[User, ArtistProfile, ArtistApplication]:
    user = User.objects.create_user(email=f"artist-{suffix}@example.com", full_name="Ana Ink")
    role, _ = Role.objects.get_or_create(code=RoleType.ARTIST, defaults={"name": "Artist"})
    UserRole.objects.create(user=user, role=role)
    profile = ArtistProfile.objects.create(
        user=user,
        professional_name="Ana Ink",
        styles=["blackwork"],
        years_experience=6,
        minimum_tattoo_value=Decimal("500"),
        expected_ticket=Decimal("900"),
    )
    application = ArtistApplication.objects.create(artist=profile)
    return user, profile, application


def build_advisory(suffix: str) -> User:
    user = User.objects.create_user(email=f"advisory-{suffix}@example.com", full_name="Ops Lead")
    role, _ = Role.objects.get_or_create(code=RoleType.ADVISORY, defaults={"name": "Advisory"})
    UserRole.objects.create(user=user, role=role)
    return user


@pytest.mark.django_db
def test_artist_without_profile_receives_not_found_instead_of_error() -> None:
    user = User.objects.create_user(email="new-artist@example.com", full_name="New Artist")
    role, _ = Role.objects.get_or_create(code=RoleType.ARTIST, defaults={"name": "Artist"})
    UserRole.objects.create(user=user, role=role)
    client = APIClient()
    client.force_authenticate(user)

    profile = client.get("/api/v1/artists/me/")
    application = client.get("/api/v1/artists/me/application/")

    assert profile.status_code == 404
    assert application.status_code == 404


@pytest.mark.django_db
def test_saving_the_profile_opens_a_draft_application() -> None:
    user = User.objects.create_user(email="draft-artist@example.com", full_name="Draft Artist")
    role, _ = Role.objects.get_or_create(code=RoleType.ARTIST, defaults={"name": "Artist"})
    UserRole.objects.create(user=user, role=role)
    client = APIClient()
    client.force_authenticate(user)

    saved = client.put(
        "/api/v1/artists/me/",
        {
            "professional_name": "Draft Artist",
            "biography": "Ten years of fine line work.",
            "years_experience": 10,
            "styles": ["fine line"],
            "currency": "BRL",
            "minimum_tattoo_value": "600.00",
            "expected_ticket": "1100.00",
        },
        format="json",
    )
    application = client.get("/api/v1/artists/me/application/")

    assert saved.status_code == 200
    assert application.status_code == 200
    assert application.data["status"] == ApplicationStatus.DRAFT


@pytest.mark.django_db
def test_incomplete_profile_is_rejected_without_creating_records() -> None:
    user = User.objects.create_user(email="partial@example.com", full_name="Partial Artist")
    role, _ = Role.objects.get_or_create(code=RoleType.ARTIST, defaults={"name": "Artist"})
    UserRole.objects.create(user=user, role=role)
    client = APIClient()
    client.force_authenticate(user)

    response = client.put(
        "/api/v1/artists/me/",
        {"professional_name": "Partial Artist"},
        format="json",
    )

    assert response.status_code == 400
    assert not ArtistProfile.objects.filter(user=user).exists()
    assert not ArtistApplication.objects.filter(artist__user=user).exists()


@pytest.mark.django_db
def test_artist_submits_and_advisory_approves_the_application() -> None:
    artist_user, _, application = build_artist("journey")
    advisory = build_advisory("journey")
    artist_client = APIClient()
    artist_client.force_authenticate(artist_user)
    advisory_client = APIClient()
    advisory_client.force_authenticate(advisory)

    submitted = artist_client.post("/api/v1/artists/me/application/")
    queue = advisory_client.get("/api/v1/operations/queues/artist-applications/")
    detail = advisory_client.get(f"/api/v1/artists/applications/{application.id}/")
    approved = advisory_client.post(
        f"/api/v1/artists/applications/{application.id}/review/",
        {"approved": True, "reason": "Portfolio approved."},
        format="json",
    )

    assert submitted.status_code == 200
    assert submitted.data["status"] == ApplicationStatus.UNDER_REVIEW
    assert queue.data["count"] == 1
    assert queue.data["results"][0]["professional_name"] == "Ana Ink"
    assert queue.data["results"][0]["styles"] == ["blackwork"]
    assert detail.status_code == 200
    assert detail.data["contact_email"] == artist_user.email
    assert detail.data["artist"]["professional_name"] == "Ana Ink"
    assert approved.status_code == 200
    assert approved.data["status"] == ApplicationStatus.APPROVED


@pytest.mark.django_db
def test_detail_exposes_portfolio_in_declared_order() -> None:
    _, profile, application = build_artist("portfolio")
    advisory = build_advisory("portfolio")
    PortfolioItem.objects.create(
        artist=profile,
        object_key="portfolio/second.jpg",
        original_name="second.jpg",
        content_type="image/jpeg",
        size_bytes=2048,
        position=2,
    )
    PortfolioItem.objects.create(
        artist=profile,
        object_key="portfolio/first.jpg",
        original_name="first.jpg",
        content_type="image/jpeg",
        size_bytes=1024,
        position=1,
    )
    client = APIClient()
    client.force_authenticate(advisory)

    response = client.get(f"/api/v1/artists/applications/{application.id}/")

    assert [item["original_name"] for item in response.data["portfolio"]] == [
        "first.jpg",
        "second.jpg",
    ]


@pytest.mark.django_db
def test_rejection_without_reason_is_refused() -> None:
    _, _, application = build_artist("rejection")
    advisory = build_advisory("rejection")
    application.status = ApplicationStatus.UNDER_REVIEW
    application.save(update_fields=["status"])
    client = APIClient()
    client.force_authenticate(advisory)

    response = client.post(
        f"/api/v1/artists/applications/{application.id}/review/",
        {"approved": False, "reason": "   "},
        format="json",
    )

    assert response.status_code == 409
    application.refresh_from_db()
    assert application.status == ApplicationStatus.UNDER_REVIEW


@pytest.mark.django_db
def test_artist_cannot_read_or_review_applications_of_the_queue() -> None:
    artist_user, _, application = build_artist("isolation")
    client = APIClient()
    client.force_authenticate(artist_user)

    detail = client.get(f"/api/v1/artists/applications/{application.id}/")
    review = client.post(
        f"/api/v1/artists/applications/{application.id}/review/",
        {"approved": True},
        format="json",
    )

    assert detail.status_code == 403
    assert review.status_code == 403
