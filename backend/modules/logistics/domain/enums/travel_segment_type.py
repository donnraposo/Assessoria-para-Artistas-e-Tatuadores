from django.db import models


class TravelSegmentType(models.TextChoices):
    OUTBOUND = "OUTBOUND", "Outbound"
    RETURN = "RETURN", "Return"
    OTHER = "OTHER", "Other"
