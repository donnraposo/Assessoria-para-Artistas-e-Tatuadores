from django.db import transaction

from modules.audit.infrastructure.persistence.models import AuditEvent
from modules.studios.domain.enums import BookingStatus, StudioStatus
from modules.studios.infrastructure.persistence.models import StudioBooking, StudioBookingRequest


class StudioBookingService:
    @staticmethod
    @transaction.atomic
    def respond(
        request: StudioBookingRequest,
        accepted: bool,
        reason: str = "",
    ) -> StudioBookingRequest:
        if request.status != BookingStatus.REQUESTED:
            raise ValueError("The request has already been answered.")
        if request.studio.status != StudioStatus.APPROVED:
            raise ValueError("The Studio must be approved.")
        request.status = BookingStatus.ACCEPTED if accepted else BookingStatus.DECLINED
        request.response_reason = reason.strip()
        request.save(update_fields=["status", "response_reason", "updated_at"])
        return request

    @staticmethod
    @transaction.atomic
    def confirm(request: StudioBookingRequest, advisory_user) -> StudioBooking:
        locked = StudioBookingRequest.objects.select_for_update().get(pk=request.pk)
        if locked.status != BookingStatus.ACCEPTED:
            raise ValueError("Only accepted requests can be confirmed.")
        conflict = StudioBooking.objects.filter(
            request__studio=locked.studio,
            request__starts_at__lt=locked.ends_at,
            request__ends_at__gt=locked.starts_at,
        ).exists()
        if conflict:
            raise ValueError("The Studio already has a conflicting booking.")
        locked.status = BookingStatus.CONFIRMED
        locked.save(update_fields=["status", "updated_at"])
        booking = StudioBooking.objects.create(request=locked, confirmed_by=advisory_user)
        AuditEvent.objects.create(
            actor=advisory_user,
            action="studio_booking.confirmed",
            resource_type="StudioBooking",
            resource_id=str(booking.id),
        )
        return booking
