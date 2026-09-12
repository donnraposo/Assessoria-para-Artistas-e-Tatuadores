from datetime import timedelta
from decimal import Decimal

import pytest
from rest_framework.test import APIClient

from modules.guests.domain.enums import GuestStatus
from modules.identity.domain.enums import RoleType
from modules.identity.infrastructure.persistence.models import Role, User, UserRole
from modules.logistics.application.services import (
    AccommodationService,
    MyTripService,
    TravelSegmentService,
)
from modules.logistics.domain.enums import LogisticsStatus, MyTripStatus, TravelSegmentType
from modules.marketing.application.services import CampaignService
from tests.sales.test_closing import build_scenario


@pytest.mark.django_db
def test_my_trip_consolidates_logistics_schedule_studios_and_costs() -> None:
    _, advisory, guest, _, appointment = build_scenario("trip")
    studio = appointment.studio
    studio.offers_accommodation = True
    studio.save(update_fields=["offers_accommodation"])
    segment = TravelSegmentService.create(
        guest=guest,
        segment_type=TravelSegmentType.OUTBOUND,
        origin="Rio de Janeiro",
        destination="Sao Paulo",
        departs_at=appointment.starts_at - timedelta(hours=4),
        arrives_at=appointment.starts_at - timedelta(hours=2),
        origin_timezone="America/Sao_Paulo",
        destination_timezone="America/Sao_Paulo",
        cost=Decimal("200.00"),
        currency="BRL",
        private_document_key="private/trip/ticket.pdf",
        actor=advisory,
    )
    accommodation = AccommodationService.create(
        guest=guest,
        studio=studio,
        name="Studio apartment",
        address="Central Street, 2",
        check_in_at=appointment.starts_at - timedelta(hours=3),
        check_out_at=appointment.ends_at + timedelta(days=1),
        timezone="America/Sao_Paulo",
        cost=Decimal("300.00"),
        currency="BRL",
        actor=advisory,
    )
    campaign = CampaignService.create(
        guest=guest,
        name="Trip campaign",
        channel="Meta Ads",
        authorized_budget=Decimal("150.00"),
        currency="BRL",
        starts_on=guest.starts_on,
        ends_on=guest.ends_on,
        actor=advisory,
    )
    CampaignService.add_spend(
        campaign=campaign,
        amount=Decimal("100.00"),
        currency="BRL",
        spent_on=guest.starts_on,
        actor=advisory,
    )

    pending_trip = MyTripService.build(guest)
    assert pending_trip["status"] == MyTripStatus.PENDING
    assert pending_trip["costs"]["total"] == Decimal("600.00")
    assert pending_trip["studios"].count() == 1
    assert pending_trip["appointments"].count() == 1

    TravelSegmentService.update(
        segment=segment,
        actor=advisory,
        status=LogisticsStatus.CONFIRMED,
    )
    AccommodationService.update(
        accommodation=accommodation,
        actor=advisory,
        status=LogisticsStatus.CONFIRMED,
    )
    assert MyTripService.build(guest)["status"] == MyTripStatus.UPDATED


@pytest.mark.django_db
def test_logistics_rejects_currency_outside_guest_currency() -> None:
    _, advisory, guest, _, appointment = build_scenario("trip-currency")
    with pytest.raises(ValueError, match="currency"):
        TravelSegmentService.create(
            guest=guest,
            segment_type=TravelSegmentType.RETURN,
            origin="Sao Paulo",
            destination="Rio de Janeiro",
            departs_at=appointment.ends_at,
            arrives_at=appointment.ends_at + timedelta(hours=2),
            origin_timezone="America/Sao_Paulo",
            destination_timezone="America/Sao_Paulo",
            cost=Decimal("200.00"),
            currency="USD",
            actor=advisory,
        )


@pytest.mark.django_db
def test_cancelled_guest_has_unavailable_my_trip() -> None:
    _, _, guest, _, _ = build_scenario("trip-cancelled")
    guest.status = GuestStatus.CANCELLED
    guest.save(update_fields=["status"])
    assert MyTripService.build(guest)["status"] == MyTripStatus.UNAVAILABLE


@pytest.mark.django_db
def test_artist_can_read_only_their_own_my_trip() -> None:
    artist_user, _, guest, _, _ = build_scenario("trip-access")
    artist_role = Role.objects.create(code=RoleType.ARTIST, name="Artist")
    UserRole.objects.create(user=artist_user, role=artist_role)
    other_artist = User.objects.create_user(
        email="unrelated-artist@example.com",
        full_name="Unrelated Artist",
    )
    UserRole.objects.create(user=other_artist, role=artist_role)
    client = APIClient()

    client.force_authenticate(artist_user)
    own_response = client.get(f"/api/v1/logistics/guests/{guest.id}/my-trip/")
    write_response = client.post(
        f"/api/v1/logistics/guests/{guest.id}/travel-segments/",
        {},
        format="json",
    )
    client.force_authenticate(other_artist)
    other_response = client.get(f"/api/v1/logistics/guests/{guest.id}/my-trip/")

    assert own_response.status_code == 200
    assert own_response.data["status"] == MyTripStatus.EMPTY
    assert write_response.status_code == 403
    assert other_response.status_code == 403
    assert "private_document_key" not in str(own_response.data)
