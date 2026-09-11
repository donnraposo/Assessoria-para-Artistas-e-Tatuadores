from django.db import models


class FinancialEntryStatus(models.TextChoices):
    CONFIRMED = "CONFIRMED", "Confirmed"
    EXPECTED = "EXPECTED", "Expected"
    DUE = "DUE", "Due"
