from django.db import transaction

from modules.audit.infrastructure.persistence.models import AuditEvent
from modules.guests.domain.enums import ProposalStatus
from modules.guests.infrastructure.persistence.models import GuestProposal

CLOSING_STATUSES = {ProposalStatus.DECLINED, ProposalStatus.CANCELLED}


class ProposalTransitionService:
    transitions = {
        ProposalStatus.DRAFT: CLOSING_STATUSES,
        ProposalStatus.PLANNING: CLOSING_STATUSES,
        ProposalStatus.READY: CLOSING_STATUSES,
        ProposalStatus.CONFIRMED: set(),
        ProposalStatus.DECLINED: set(),
        ProposalStatus.CANCELLED: set(),
    }

    @classmethod
    @transaction.atomic
    def transition(
        cls, proposal: GuestProposal, target: str, actor, reason: str = ""
    ) -> GuestProposal:
        locked = GuestProposal.objects.select_for_update().get(pk=proposal.pk)
        if target not in cls.transitions.get(locked.status, set()):
            raise ValueError("Invalid Proposal status transition.")
        if not reason.strip():
            raise ValueError(f"Moving a proposal to {target} requires a reason.")
        previous = locked.status
        locked.status = target
        locked.save(update_fields=["status", "updated_at"])
        AuditEvent.objects.create(
            actor=actor,
            action="guest_proposal.status_changed",
            resource_type="GuestProposal",
            resource_id=str(locked.id),
            reason=reason.strip(),
            changes={"status": {"from": previous, "to": target}},
        )
        return locked
