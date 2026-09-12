from django.core.paginator import Paginator
from django.db.models import OuterRef, Subquery

from modules.artists.domain.enums import ApplicationStatus
from modules.artists.infrastructure.persistence.models import ArtistApplication
from modules.guests.domain.enums import ProposalStatus
from modules.guests.infrastructure.persistence.models import GuestProposal
from modules.logistics.domain.enums import LogisticsStatus
from modules.logistics.infrastructure.persistence.models import Accommodation, TravelSegment
from modules.sales.domain.enums import LeadStatus
from modules.sales.infrastructure.persistence.models import Lead
from modules.scheduling.domain.enums import AppointmentStatus, CancellationStatus
from modules.scheduling.infrastructure.persistence.models import Appointment, CancellationRequest
from modules.studios.domain.enums import BookingStatus, StudioStatus
from modules.studios.infrastructure.persistence.models import Studio, StudioBookingRequest


class OperationsQueueService:
    @staticmethod
    def get(queue_name: str, page_number: int, page_size: int) -> dict:
        if queue_name == "logistics":
            return OperationsQueueService._get_logistics(page_number, page_size)
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
            "open-leads": Lead.objects.filter(status=LeadStatus.OPEN)
            .annotate(
                appointment_id=Subquery(
                    Appointment.objects.filter(
                        guest_id=OuterRef("guest_id"),
                        client_name=OuterRef("client_name"),
                        status=AppointmentStatus.PENDING_PAYMENT,
                    ).values("id")[:1]
                )
            )
            .values(
                "id",
                "guest_id",
                "appointment_id",
                "client_name",
                "source",
                "status",
                "created_at",
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

    @staticmethod
    def _get_logistics(page_number: int, page_size: int) -> dict:
        travel = TravelSegment.objects.filter(status=LogisticsStatus.PENDING).values(
            "id",
            "guest_id",
            "status",
            "origin",
            "destination",
            "updated_at",
        )
        accommodations = Accommodation.objects.filter(status=LogisticsStatus.PENDING).values(
            "id",
            "guest_id",
            "status",
            "name",
            "updated_at",
        )
        results = [
            {**item, "item_type": "Travel segment"} for item in travel
        ] + [{**item, "item_type": "Accommodation"} for item in accommodations]
        results.sort(key=lambda item: item["updated_at"], reverse=True)
        paginator = Paginator(results, per_page=min(max(page_size, 1), 100))
        page = paginator.get_page(max(page_number, 1))
        return {
            "count": paginator.count,
            "page": page.number,
            "pages": paginator.num_pages,
            "results": list(page.object_list),
        }
