from django.db.models import Sum

from modules.artists.domain.enums import ApplicationStatus
from modules.artists.infrastructure.persistence.models import ArtistApplication
from modules.audit.infrastructure.persistence.models import AuditEvent
from modules.finance.domain.enums import FinancialEntryStatus, FinancialEntryType
from modules.finance.infrastructure.persistence.models import FinancialEntry
from modules.guests.domain.enums import ProposalStatus
from modules.guests.infrastructure.persistence.models import GuestProposal
from modules.logistics.domain.enums import LogisticsStatus
from modules.logistics.infrastructure.persistence.models import Accommodation, TravelSegment
from modules.notifications.infrastructure.persistence.models import Notification
from modules.sales.domain.enums import LeadStatus
from modules.sales.infrastructure.persistence.models import Lead
from modules.scheduling.domain.enums import CancellationStatus
from modules.scheduling.infrastructure.persistence.models import CancellationRequest
from modules.studios.domain.enums import BookingStatus, StudioStatus
from modules.studios.infrastructure.persistence.models import Studio, StudioBookingRequest


class OperationsDashboardService:
    @staticmethod
    def build(user) -> dict:
        agency_revenue_by_currency = list(
            FinancialEntry.objects.filter(
                entry_type=FinancialEntryType.AGENCY_REVENUE,
                status=FinancialEntryStatus.CONFIRMED,
            )
            .values("currency")
            .annotate(total=Sum("amount"))
            .order_by("currency")
        )
        return {
            "queues": {
                "artist_applications": ArtistApplication.objects.filter(
                    status=ApplicationStatus.UNDER_REVIEW
                ).count(),
                "studios": Studio.objects.filter(status=StudioStatus.UNDER_REVIEW).count(),
                "guest_proposals": GuestProposal.objects.filter(
                    status__in=[ProposalStatus.PLANNING, ProposalStatus.READY]
                ).count(),
                "studio_reservations": StudioBookingRequest.objects.filter(
                    status__in=[BookingStatus.REQUESTED, BookingStatus.ACCEPTED]
                ).count(),
                "open_leads": Lead.objects.filter(status=LeadStatus.OPEN).count(),
                "cancellations": CancellationRequest.objects.filter(
                    status=CancellationStatus.PENDING
                ).count(),
                "logistics": TravelSegment.objects.filter(status=LogisticsStatus.PENDING).count()
                + Accommodation.objects.filter(status=LogisticsStatus.PENDING).count(),
            },
            "agency_revenue_by_currency": agency_revenue_by_currency,
            "unread_notifications": Notification.objects.filter(
                recipient=user,
                read_at__isnull=True,
            ).count(),
            "recent_activity": list(
                AuditEvent.objects.values(
                    "id",
                    "action",
                    "resource_type",
                    "resource_id",
                    "created_at",
                )[:10]
            ),
        }
