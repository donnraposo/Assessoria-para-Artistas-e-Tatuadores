from decimal import Decimal

from django.db.models import Sum

from modules.guests.domain.enums import GuestStatus
from modules.logistics.domain.enums import LogisticsStatus, MyTripStatus
from modules.logistics.infrastructure.persistence.models import Accommodation, TravelSegment
from modules.marketing.infrastructure.persistence.models import AdSpend
from modules.scheduling.domain.enums import AppointmentStatus
from modules.scheduling.infrastructure.persistence.models import Appointment


class MyTripService:
    @staticmethod
    def build(guest) -> dict:
        travel_segments = TravelSegment.objects.filter(guest=guest)
        accommodations = Accommodation.objects.filter(guest=guest)
        has_records = travel_segments.exists() or accommodations.exists()
        has_pending = travel_segments.filter(status=LogisticsStatus.PENDING).exists() or (
            accommodations.filter(status=LogisticsStatus.PENDING).exists()
        )
        if guest.status == GuestStatus.CANCELLED:
            status = MyTripStatus.UNAVAILABLE
        elif not has_records:
            status = MyTripStatus.EMPTY
        elif has_pending:
            status = MyTripStatus.PENDING
        else:
            status = MyTripStatus.UPDATED
        active_statuses = [LogisticsStatus.PENDING, LogisticsStatus.CONFIRMED]
        travel_cost = travel_segments.filter(status__in=active_statuses).aggregate(
            total=Sum("cost")
        )["total"] or Decimal("0")
        accommodation_cost = accommodations.filter(status__in=active_statuses).aggregate(
            total=Sum("cost")
        )["total"] or Decimal("0")
        ad_cost = AdSpend.objects.filter(
            campaign__guest=guest,
            currency=guest.currency,
        ).aggregate(total=Sum("amount"))["total"] or Decimal("0")
        appointments = Appointment.objects.filter(guest=guest).exclude(
            status=AppointmentStatus.CANCELLED
        )
        return {
            "status": status,
            "travel_segments": travel_segments,
            "accommodations": accommodations,
            "studios": guest.studios.select_related("studio").all(),
            "appointments": appointments.select_related("studio"),
            "costs": {
                "currency": guest.currency,
                "travel": travel_cost,
                "accommodation": accommodation_cost,
                "ads": ad_cost,
                "total": travel_cost + accommodation_cost + ad_cost,
            },
        }
