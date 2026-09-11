from decimal import ROUND_HALF_UP, Decimal

from django.db import connection, transaction

from modules.audit.infrastructure.persistence.models import AuditEvent
from modules.finance.domain.enums import FinancialEntryStatus, FinancialEntryType
from modules.finance.infrastructure.persistence.models import AgencyReceipt, FinancialEntry
from modules.sales.domain.enums import LeadStatus
from modules.sales.infrastructure.persistence.models import Closing, Lead
from modules.scheduling.domain.enums import AppointmentStatus
from modules.scheduling.infrastructure.persistence.models import Appointment


class ClosingService:
    agency_rate = Decimal("0.20")

    @classmethod
    @transaction.atomic
    def close(
        cls,
        *,
        lead: Lead,
        appointment: Appointment,
        actor,
        final_value: Decimal,
        currency: str,
        artist_minimum_approved: bool,
        payment_reference: str,
        idempotency_key: str,
    ) -> Closing:
        existing = (
            AgencyReceipt.objects.select_related("closing")
            .filter(idempotency_key=idempotency_key)
            .first()
        )
        if existing:
            closing = existing.closing
            if (
                closing.lead_id != lead.id
                or closing.appointment_id != appointment.id
                or closing.final_value != final_value
                or closing.currency != currency
            ):
                raise ValueError("The idempotency key was already used for another closing.")
            return closing

        locked_lead = Lead.objects.select_for_update().get(pk=lead.pk)
        locked_appointment = Appointment.objects.select_for_update().get(pk=appointment.pk)
        if locked_lead.status != LeadStatus.OPEN:
            raise ValueError("The Lead is no longer open.")
        if locked_appointment.status != AppointmentStatus.PENDING_PAYMENT:
            raise ValueError("The appointment is not awaiting payment.")
        if locked_lead.guest_id != locked_appointment.guest_id:
            raise ValueError("The Lead and appointment must belong to the same Guest.")
        guest = locked_lead.guest
        if currency != guest.currency or currency != locked_appointment.currency:
            raise ValueError("The closing currency must match the Guest currency.")
        minimum = guest.proposal.minimum_tattoo_value
        if final_value < minimum:
            raise ValueError("The closing value cannot be below the Artist minimum.")
        if final_value == minimum and not artist_minimum_approved:
            raise ValueError("Artist approval is required when closing at the minimum value.")
        if not payment_reference.strip():
            raise ValueError("A payment reference is required.")

        cls._lock_artist_schedule(str(locked_appointment.artist_id))
        has_conflict = (
            Appointment.objects.filter(
                artist=locked_appointment.artist,
                starts_at__lt=locked_appointment.ends_at,
                ends_at__gt=locked_appointment.starts_at,
                status__in=[
                    AppointmentStatus.CONFIRMED,
                    AppointmentStatus.CANCELLATION_REQUESTED,
                ],
            )
            .exclude(pk=locked_appointment.pk)
            .exists()
        )
        if has_conflict:
            raise ValueError("The Artist already has a conflicting confirmed appointment.")

        closing = Closing.objects.create(
            lead=locked_lead,
            appointment=locked_appointment,
            final_value=final_value,
            currency=currency,
            artist_minimum_approved=artist_minimum_approved,
            closed_by=actor,
        )
        agency_amount = (final_value * cls.agency_rate).quantize(
            Decimal("0.01"), rounding=ROUND_HALF_UP
        )
        artist_amount = final_value - agency_amount
        receipt = AgencyReceipt.objects.create(
            closing=closing,
            amount=agency_amount,
            currency=currency,
            external_reference=payment_reference.strip(),
            idempotency_key=idempotency_key,
        )
        FinancialEntry.objects.bulk_create(
            [
                FinancialEntry(
                    guest=guest,
                    closing=closing,
                    entry_type=FinancialEntryType.AGENCY_REVENUE,
                    status=FinancialEntryStatus.CONFIRMED,
                    amount=agency_amount,
                    currency=currency,
                    source_reference=f"receipt:{receipt.id}",
                ),
                FinancialEntry(
                    guest=guest,
                    closing=closing,
                    entry_type=FinancialEntryType.ARTIST_RECEIVABLE,
                    status=FinancialEntryStatus.EXPECTED,
                    amount=artist_amount,
                    currency=currency,
                    source_reference=f"closing:{closing.id}",
                ),
            ]
        )
        locked_lead.status = LeadStatus.CLOSED
        locked_lead.save(update_fields=["status", "updated_at"])
        locked_appointment.final_value = final_value
        locked_appointment.status = AppointmentStatus.CONFIRMED
        locked_appointment.save(update_fields=["final_value", "status", "updated_at"])
        AuditEvent.objects.create(
            actor=actor,
            action="closing.confirmed",
            resource_type="Closing",
            resource_id=str(closing.id),
            changes={
                "appointment_status": AppointmentStatus.CONFIRMED,
                "agency_amount": str(agency_amount),
                "artist_amount": str(artist_amount),
                "currency": currency,
            },
        )
        return closing

    @staticmethod
    def _lock_artist_schedule(artist_id: str) -> None:
        with connection.cursor() as cursor:
            cursor.execute("SELECT pg_advisory_xact_lock(hashtext(%s))", [artist_id])
