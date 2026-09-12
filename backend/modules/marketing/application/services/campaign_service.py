from django.db import transaction

from modules.audit.infrastructure.persistence.models import AuditEvent
from modules.marketing.infrastructure.persistence.models import AdSpend, Campaign


class CampaignService:
    @staticmethod
    @transaction.atomic
    def create(*, actor, **data) -> Campaign:
        guest = data["guest"]
        if data["ends_on"] < data["starts_on"]:
            raise ValueError("The campaign end date must not precede its start date.")
        if data["currency"] != guest.currency:
            raise ValueError("The campaign currency must match the Guest currency.")
        campaign = Campaign.objects.create(created_by=actor, **data)
        AuditEvent.objects.create(
            actor=actor,
            action="campaign.created",
            resource_type="Campaign",
            resource_id=str(campaign.id),
            changes={"authorized_budget": str(campaign.authorized_budget)},
        )
        return campaign

    @staticmethod
    @transaction.atomic
    def add_spend(*, campaign: Campaign, actor, **data) -> AdSpend:
        locked = Campaign.objects.select_for_update().get(pk=campaign.pk)
        if data["currency"] != locked.currency:
            raise ValueError("The Ad spend currency must match the campaign currency.")
        if not locked.starts_on <= data["spent_on"] <= locked.ends_on:
            raise ValueError("The Ad spend date must be within the campaign period.")
        spend = AdSpend.objects.create(campaign=locked, recorded_by=actor, **data)
        AuditEvent.objects.create(
            actor=actor,
            action="campaign.spend_recorded",
            resource_type="AdSpend",
            resource_id=str(spend.id),
            changes={"amount": str(spend.amount), "currency": spend.currency},
        )
        return spend
