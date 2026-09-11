from datetime import datetime, time, timedelta
from decimal import Decimal
from zoneinfo import ZoneInfo

from modules.artists.infrastructure.persistence.models import ArtistAvailability
from modules.scheduling.domain.enums import AppointmentStatus
from modules.scheduling.infrastructure.persistence.models import Appointment


class OccupancyService:
    @staticmethod
    def calculate(guest) -> dict:
        zone = ZoneInfo(guest.timezone)
        guest_starts_at = datetime.combine(guest.starts_on, time.min, tzinfo=zone)
        guest_ends_at = datetime.combine(
            guest.ends_on + timedelta(days=1),
            time.min,
            tzinfo=zone,
        )
        availabilities = ArtistAvailability.objects.filter(
            artist=guest.artist,
            starts_at__lt=guest_ends_at,
            ends_at__gt=guest_starts_at,
        )
        appointments = Appointment.objects.filter(
            guest=guest,
            status__in=[AppointmentStatus.CONFIRMED, AppointmentStatus.COMPLETED],
        )
        available_intervals = [
            (max(item.starts_at, guest_starts_at), min(item.ends_at, guest_ends_at))
            for item in availabilities
        ]
        available_seconds = sum(
            (ends_at - starts_at).total_seconds() for starts_at, ends_at in available_intervals
        )
        booked_seconds = sum(
            (item.ends_at - item.starts_at).total_seconds() for item in appointments
        )
        available_days = {starts_at.astimezone(zone).date() for starts_at, _ in available_intervals}
        booked_days = {item.starts_at.astimezone(zone).date() for item in appointments}
        hour_rate = Decimal("0")
        day_rate = Decimal("0")
        if available_seconds:
            hour_rate = Decimal(str(booked_seconds / available_seconds * 100)).quantize(
                Decimal("0.01")
            )
        if available_days:
            day_rate = Decimal(len(booked_days) * 100 / len(available_days)).quantize(
                Decimal("0.01")
            )
        return {
            "available_hours": Decimal(str(available_seconds / timedelta(hours=1).total_seconds())),
            "booked_hours": Decimal(str(booked_seconds / timedelta(hours=1).total_seconds())),
            "hour_occupancy_percentage": hour_rate,
            "available_days": len(available_days),
            "booked_days": len(booked_days),
            "day_occupancy_percentage": day_rate,
        }
