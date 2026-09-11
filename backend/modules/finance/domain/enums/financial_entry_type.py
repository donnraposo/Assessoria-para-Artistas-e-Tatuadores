from django.db import models


class FinancialEntryType(models.TextChoices):
    AGENCY_REVENUE = "AGENCY_REVENUE", "Agency revenue"
    ARTIST_RECEIVABLE = "ARTIST_RECEIVABLE", "Artist receivable"
    ARTIST_REFUND_DUE = "ARTIST_REFUND_DUE", "Artist refund due"
