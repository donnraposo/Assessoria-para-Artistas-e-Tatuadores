from django.db import transaction
from django.utils import timezone

from modules.audit.infrastructure.persistence.models import AuditEvent
from modules.finance.domain.enums import FinancialEntryStatus, FinancialEntryType
from modules.finance.infrastructure.persistence.models import AgencyReceipt, FinancialEntry
from modules.notifications.application.services import NotificationService
from modules.sales.infrastructure.persistence.models import Closing
from modules.scheduling.domain.enums import (
    AppointmentStatus,
    CancellationResponsibility,
    CancellationStatus,
)
from modules.scheduling.infrastructure.persistence.models import Appointment, CancellationRequest


class CancellationService:
    @staticmethod
    @transaction.atomic
    def request(*, appointment: Appointment, actor, reason: str) -> CancellationRequest:
        locked = Appointment.objects.select_for_update().get(pk=appointment.pk)
        if locked.artist.user_id != actor.id:
            raise ValueError("Only the assigned Artist can request this cancellation.")
        if locked.status != AppointmentStatus.CONFIRMED:
            raise ValueError("Only confirmed appointments can have cancellation requests.")
        if not reason.strip():
            raise ValueError("A cancellation reason is required.")
        cancellation = CancellationRequest.objects.create(
            appointment=locked,
            requested_by=actor,
            responsibility=CancellationResponsibility.ARTIST,
            reason=reason.strip(),
        )
        locked.status = AppointmentStatus.CANCELLATION_REQUESTED
        locked.save(update_fields=["status", "updated_at"])
        AuditEvent.objects.create(
            actor=actor,
            action="appointment.cancellation_requested",
            resource_type="CancellationRequest",
            resource_id=str(cancellation.id),
            reason=reason.strip(),
        )
        return cancellation

    @staticmethod
    @transaction.atomic
    def decide(
        *, cancellation: CancellationRequest, actor, approved: bool, reason: str = ""
    ) -> CancellationRequest:
        locked = CancellationRequest.objects.select_for_update().get(pk=cancellation.pk)
        if locked.status != CancellationStatus.PENDING:
            raise ValueError("The cancellation request has already been decided.")
        appointment = Appointment.objects.select_for_update().get(pk=locked.appointment_id)
        locked.status = CancellationStatus.APPROVED if approved else CancellationStatus.REJECTED
        locked.decided_by = actor
        locked.decision_reason = reason.strip()
        locked.decided_at = timezone.now()
        locked.save(update_fields=["status", "decided_by", "decision_reason", "decided_at"])
        appointment.status = (
            AppointmentStatus.CANCELLED if approved else AppointmentStatus.CONFIRMED
        )
        appointment.save(update_fields=["status", "updated_at"])
        if approved and locked.responsibility == CancellationResponsibility.ARTIST:
            closing = Closing.objects.get(appointment=appointment)
            receipt = AgencyReceipt.objects.get(closing=closing)
            FinancialEntry.objects.create(
                guest=appointment.guest,
                closing=closing,
                entry_type=FinancialEntryType.ARTIST_REFUND_DUE,
                status=FinancialEntryStatus.DUE,
                amount=receipt.amount,
                currency=receipt.currency,
                source_reference=f"cancellation:{locked.id}",
            )
        AuditEvent.objects.create(
            actor=actor,
            action="appointment.cancellation_decided",
            resource_type="CancellationRequest",
            resource_id=str(locked.id),
            reason=reason.strip(),
            changes={"approved": approved, "appointment_status": appointment.status},
        )
        NotificationService.enqueue(
            recipient=appointment.artist.user,
            category="appointment_cancellation",
            subject="Appointment cancellation decision",
            message=(
                "Your cancellation request was approved."
                if approved
                else "Your cancellation request was not approved."
            ),
            key=f"cancellation-decision:{locked.id}",
        )
        return locked
