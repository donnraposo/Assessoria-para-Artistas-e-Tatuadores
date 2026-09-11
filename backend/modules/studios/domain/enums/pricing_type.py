from django.db import models


class PricingType(models.TextChoices):
    HOURLY = "HOURLY", "Hourly"
    DAILY = "DAILY", "Daily"
    WEEKLY = "WEEKLY", "Weekly"
    PERCENTAGE = "PERCENTAGE", "Percentage"
    NEGOTIATED = "NEGOTIATED", "Negotiated"
