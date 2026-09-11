from datetime import timedelta
from decimal import Decimal

import pytest

from modules.scheduling.application.services import AppointmentService, OccupancyService
from modules.scheduling.domain.enums import AppointmentStatus
from tests.sales.test_closing import build_scenario


@pytest.mark.django_db
def test_occupancy_is_calculated_by_hours_and_days() -> None:
    _, _, guest, _, appointment = build_scenario("occupancy")
    appointment.status = AppointmentStatus.CONFIRMED
    appointment.save(update_fields=["status"])

    result = OccupancyService.calculate(guest)

    assert result["available_hours"] == Decimal("8.0")
    assert result["booked_hours"] == Decimal("4.0")
    assert result["hour_occupancy_percentage"] == Decimal("50.00")
    assert result["day_occupancy_percentage"] == Decimal("100.00")


@pytest.mark.django_db
def test_appointment_outside_artist_availability_is_rejected() -> None:
    _, advisory, guest, _, appointment = build_scenario("outside")
    with pytest.raises(ValueError, match="outside"):
        AppointmentService.create(
            guest=guest,
            studio=appointment.studio,
            client_name="Late Client",
            starts_at=appointment.starts_at + timedelta(hours=7),
            ends_at=appointment.starts_at + timedelta(hours=9),
            timezone=guest.timezone,
            currency=guest.currency,
            actor=advisory,
        )
