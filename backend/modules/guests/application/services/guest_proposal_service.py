from datetime import datetime
from zoneinfo import ZoneInfo

from django.db import transaction
from django.utils import timezone

from modules.artists.domain.enums import ApplicationStatus
from modules.artists.infrastructure.persistence.models import ArtistApplication
from modules.audit.infrastructure.persistence.models import AuditEvent
from modules.guests.domain.enums import ProposalStatus
from modules.guests.domain.policies import ArtistCommercialFloor
from modules.guests.infrastructure.persistence.models import Guest, GuestProposal, GuestStudio
from modules.studios.domain.enums import StudioStatus


class GuestProposalService:
    @staticmethod
    def mark_ready(proposal: GuestProposal) -> GuestProposal:
        if proposal.status not in {ProposalStatus.DRAFT, ProposalStatus.PLANNING}:
            raise ValueError("The proposal cannot be prepared from its current status.")
        if proposal.ends_on < proposal.starts_on:
            raise ValueError("The end date must not precede the start date.")
        if not ArtistApplication.objects.filter(
            artist=proposal.artist,
            status=ApplicationStatus.APPROVED,
        ).exists():
            raise ValueError("The Artist application must be approved.")
        if proposal.primary_studio.status != StudioStatus.APPROVED:
            raise ValueError("The primary Studio must be approved.")
        if not proposal.currency or proposal.ads_budget is None:
            raise ValueError("Currency and ad budget are required.")
        ArtistCommercialFloor.ensure_respected(
            proposal.artist.minimum_tattoo_value,
            proposal.minimum_tattoo_value,
        )
        proposal.status = ProposalStatus.READY
        proposal.save(update_fields=["status", "updated_at"])
        return proposal

    @staticmethod
    @transaction.atomic
    def confirm(proposal: GuestProposal, actor) -> Guest:
        locked = GuestProposal.objects.select_for_update().get(pk=proposal.pk)
        if locked.status != ProposalStatus.READY:
            raise ValueError("The proposal is not ready for confirmation.")
        locked.status = ProposalStatus.CONFIRMED
        locked.save(update_fields=["status", "updated_at"])
        guest = Guest.objects.create(
            proposal=locked,
            artist=locked.artist,
            city=locked.city,
            country_code=locked.country_code,
            starts_on=locked.starts_on,
            ends_on=locked.ends_on,
            timezone=locked.timezone,
            currency=locked.currency,
        )
        zone = ZoneInfo(locked.timezone)
        GuestStudio.objects.create(
            guest=guest,
            studio=locked.primary_studio,
            starts_at=timezone.make_aware(
                datetime.combine(locked.starts_on, datetime.min.time()), zone
            ),
            ends_at=timezone.make_aware(
                datetime.combine(locked.ends_on, datetime.max.time()), zone
            ),
        )
        AuditEvent.objects.create(
            actor=actor,
            action="guest.confirmed",
            resource_type="Guest",
            resource_id=str(guest.id),
            changes={"proposal_id": str(locked.id)},
        )
        return guest
