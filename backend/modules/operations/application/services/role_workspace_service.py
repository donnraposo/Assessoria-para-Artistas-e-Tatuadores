from django.db.models import Sum
from django.utils import timezone

from modules.finance.domain.enums import FinancialEntryStatus, FinancialEntryType
from modules.finance.infrastructure.persistence.models import FinancialEntry
from modules.guests.domain.enums import GuestStatus
from modules.guests.infrastructure.persistence.models import Guest
from modules.identity.domain.enums import RoleType
from modules.logistics.domain.enums import LogisticsStatus
from modules.logistics.infrastructure.persistence.models import Accommodation, TravelSegment
from modules.notifications.infrastructure.persistence.models import Notification
from modules.scheduling.domain.enums import AppointmentStatus
from modules.scheduling.infrastructure.persistence.models import Appointment
from modules.studios.domain.enums import BookingStatus
from modules.studios.infrastructure.persistence.models import StudioBooking, StudioBookingRequest


class RoleWorkspaceService:
    @staticmethod
    def build(user) -> dict:
        roles = set(user.roles.values_list("role__code", flat=True))
        if RoleType.ARTIST in roles:
            return RoleWorkspaceService._artist(user)
        if RoleType.STUDIO in roles:
            return RoleWorkspaceService._studio(user)
        raise ValueError("No supported workspace is assigned to this account.")

    @staticmethod
    def _artist(user) -> dict:
        guests = Guest.objects.filter(artist__user=user)
        pending_logistics = TravelSegment.objects.filter(
            guest__artist__user=user,
            status=LogisticsStatus.PENDING,
        ).count() + Accommodation.objects.filter(
            guest__artist__user=user,
            status=LogisticsStatus.PENDING,
        ).count()
        balances = list(
            FinancialEntry.objects.filter(
                guest__artist__user=user,
                entry_type=FinancialEntryType.ARTIST_RECEIVABLE,
                status=FinancialEntryStatus.EXPECTED,
            )
            .values("currency")
            .annotate(total=Sum("amount"))
            .order_by("currency")
        )
        return {
            "role": RoleType.ARTIST,
            "cards": [
                {
                    "key": "active_guests",
                    "label": "Active Guests",
                    "value": guests.exclude(
                        status__in=[GuestStatus.FINISHED, GuestStatus.CANCELLED]
                    ).count(),
                    "detail": "Current Guest operations",
                },
                {
                    "key": "upcoming_appointments",
                    "label": "Upcoming appointments",
                    "value": Appointment.objects.filter(
                        artist__user=user,
                        starts_at__gte=timezone.now(),
                        status__in=[
                            AppointmentStatus.CONFIRMED,
                            AppointmentStatus.CANCELLATION_REQUESTED,
                        ],
                    ).count(),
                    "detail": "Confirmed schedule",
                },
                {
                    "key": "pending_logistics",
                    "label": "Trip updates",
                    "value": pending_logistics,
                    "detail": "Pending travel information",
                },
                {
                    "key": "notifications",
                    "label": "Unread notifications",
                    "value": Notification.objects.filter(
                        recipient=user,
                        read_at__isnull=True,
                    ).count(),
                    "detail": "Operational updates",
                },
            ],
            "balances": balances,
        }

    @staticmethod
    def _studio(user) -> dict:
        return {
            "role": RoleType.STUDIO,
            "cards": [
                {
                    "key": "pending_requests",
                    "label": "Reservation requests",
                    "value": StudioBookingRequest.objects.filter(
                        studio__owner=user,
                        status=BookingStatus.REQUESTED,
                    ).count(),
                    "detail": "Awaiting your response",
                },
                {
                    "key": "accepted_requests",
                    "label": "Accepted requests",
                    "value": StudioBookingRequest.objects.filter(
                        studio__owner=user,
                        status=BookingStatus.ACCEPTED,
                    ).count(),
                    "detail": "Awaiting Advisory confirmation",
                },
                {
                    "key": "confirmed_bookings",
                    "label": "Confirmed bookings",
                    "value": StudioBooking.objects.filter(request__studio__owner=user).count(),
                    "detail": "Operational reservations",
                },
                {
                    "key": "notifications",
                    "label": "Unread notifications",
                    "value": Notification.objects.filter(
                        recipient=user,
                        read_at__isnull=True,
                    ).count(),
                    "detail": "Operational updates",
                },
            ],
            "balances": [],
        }

