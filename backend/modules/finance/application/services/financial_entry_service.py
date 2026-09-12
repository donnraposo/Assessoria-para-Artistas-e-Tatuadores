from django.db import transaction

from modules.audit.infrastructure.persistence.models import AuditEvent
from modules.finance.domain.enums import FinancialEntryStatus
from modules.finance.infrastructure.persistence.models import FinancialEntry


class FinancialEntryService:
    @staticmethod
    @transaction.atomic
    def confirm(entry: FinancialEntry, actor, reference: str = "") -> FinancialEntry:
        locked = FinancialEntry.objects.select_for_update().get(pk=entry.pk)
        if locked.status == FinancialEntryStatus.CONFIRMED:
            raise ValueError("The entry is already confirmed.")
        previous = locked.status
        locked.status = FinancialEntryStatus.CONFIRMED
        locked.save(update_fields=["status"])
        AuditEvent.objects.create(
            actor=actor,
            action="financial_entry.confirmed",
            resource_type="FinancialEntry",
            resource_id=str(locked.id),
            reason=reference.strip(),
            changes={"status": {"from": previous, "to": locked.status}},
        )
        return locked
