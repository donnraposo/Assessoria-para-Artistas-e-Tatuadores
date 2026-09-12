from django.core.paginator import Paginator

from modules.artists.domain.enums import ApplicationStatus
from modules.artists.infrastructure.persistence.models import ArtistApplication
from modules.guests.domain.enums import ProposalStatus
from modules.guests.infrastructure.persistence.models import GuestProposal
from modules.sales.domain.enums import LeadStatus
from modules.sales.infrastructure.persistence.models import Lead
from modules.scheduling.domain.enums import CancellationStatus
from modules.scheduling.infrastructure.persistence.models import CancellationRequest
from modules.studios.domain.enums import BookingStatus, StudioStatus
from modules.studios.infrastructure.persistence.models import Studio, StudioBookingRequest


class OperationsQueueService:
    @staticmethod
    def get(queue_name: str, page_number: int, page_size: int) -> dict:
        queues = {
            "artist-applications": ArtistApplication.objects.filter(
                status=ApplicationStatus.UNDER_REVIEW
            ).values("id", "artist_id", "status", "submitted_at", "updated_at"),
            "studios": Studio.objects.filter(status=StudioStatus.UNDER_REVIEW).values(
                "id", "name", "city", "country_code", "status", "updated_at"
            ),
            "guest-proposals": GuestProposal.objects.filter(
                status__in=[ProposalStatus.PLANNING, ProposalStatus.READY]
            ).values("id", "artist_id", "city", "country_code", "status", "updated_at"),
            "studio-reservations": StudioBookingRequest.objects.filter(
                status__in=[BookingStatus.REQUESTED, BookingStatus.ACCEPTED]
            ).values("id", "guest_id", "studio_id", "status", "starts_at", "ends_at"),
            "open-leads": Lead.objects.filter(status=LeadStatus.OPEN).values(
                "id", "guest_id", "client_name", "source", "status", "created_at"
            ),
            "cancellations": CancellationRequest.objects.filter(
                status=CancellationStatus.PENDING
            ).values("id", "appointment_id", "reason", "status", "created_at"),
        }
        queryset = queues.get(queue_name)
        if queryset is None:
            raise ValueError("Unknown operations queue.")
        paginator = Paginator(queryset, per_page=min(max(page_size, 1), 100))
        page = paginator.get_page(max(page_number, 1))
        return {
            "count": paginator.count,
            "page": page.number,
            "pages": paginator.num_pages,
            "results": list(page.object_list),
        }
