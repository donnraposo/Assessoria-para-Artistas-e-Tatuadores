from django.db import transaction

from modules.audit.infrastructure.persistence.models import AuditEvent
from modules.guests.domain.enums import GuestStatus
from modules.guests.infrastructure.persistence.models import Guest


class GuestTransitionService:
    transitions = {
        GuestStatus.CAPTURING: {
            GuestStatus.FULLY_BOOKED,
            GuestStatus.IN_PROGRESS,
            GuestStatus.CANCELLED,
        },
        GuestStatus.FULLY_BOOKED: {
            GuestStatus.CAPTURING,
            GuestStatus.IN_PROGRESS,
            GuestStatus.CANCELLED,
        },
        GuestStatus.IN_PROGRESS: {GuestStatus.FINISHED, GuestStatus.CANCELLED},
        GuestStatus.FINISHED: set(),
        GuestStatus.CANCELLED: set(),
    }

    @classmethod
    @transaction.atomic
    def transition(cls, guest: Guest, target: str, actor, reason: str = "") -> Guest:
        locked = Guest.objects.select_for_update().get(pk=guest.pk)
        if target not in cls.transitions[locked.status]:
            raise ValueError("Invalid Guest status transition.")
        if target == GuestStatus.CANCELLED and not reason.strip():
            raise ValueError("Cancellation requires a reason.")
        previous = locked.status
        locked.status = target
        locked.save(update_fields=["status", "updated_at"])
        AuditEvent.objects.create(
            actor=actor,
            action="guest.status_changed",
            resource_type="Guest",
            resource_id=str(locked.id),
            reason=reason.strip(),
            changes={"status": {"from": previous, "to": target}},
        )
        return locked
