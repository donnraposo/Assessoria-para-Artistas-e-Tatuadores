from django.db import transaction

from modules.audit.infrastructure.persistence.models import AuditEvent
from modules.studios.domain.enums import BookingStatus, StudioStatus
from modules.studios.infrastructure.persistence.models import StudioBooking, StudioBookingRequest

PAYMENT_STATUSES = {"PENDING", "PAID"}


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
    def register_external_response(
        request: StudioBookingRequest,
        actor,
        accepted: bool,
        reason: str,
    ) -> StudioBookingRequest:
        if not reason.strip():
            raise ValueError(
                "Registering an externally negotiated response requires a reason."
            )
        updated = StudioBookingService.respond(request, accepted, reason)
        AuditEvent.objects.create(
            actor=actor,
            action="studio_booking.external_response_registered",
            resource_type="StudioBookingRequest",
            resource_id=str(updated.id),
            reason=reason.strip(),
            changes={"status": updated.status},
        )
        return updated

    @staticmethod
    @transaction.atomic
    def update_payment_status(
        booking: StudioBooking,
        actor,
        payment_status: str,
    ) -> StudioBooking:
        if payment_status not in PAYMENT_STATUSES:
            raise ValueError("Invalid payment status.")
        locked = StudioBooking.objects.select_for_update().get(pk=booking.pk)
        previous = locked.payment_status
        locked.payment_status = payment_status
        locked.save(update_fields=["payment_status"])
        AuditEvent.objects.create(
            actor=actor,
            action="studio_booking.payment_status_changed",
            resource_type="StudioBooking",
            resource_id=str(locked.id),
            changes={"payment_status": {"from": previous, "to": payment_status}},
        )
        return locked

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
