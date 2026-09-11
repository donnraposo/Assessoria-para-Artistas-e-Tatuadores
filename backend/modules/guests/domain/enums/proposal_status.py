from django.db import models


class ProposalStatus(models.TextChoices):
    DRAFT = "DRAFT", "Draft"
    PLANNING = "PLANNING", "Planning"
    READY = "READY", "Ready for confirmation"
    CONFIRMED = "CONFIRMED", "Confirmed"
    DECLINED = "DECLINED", "Declined"
    CANCELLED = "CANCELLED", "Cancelled"
