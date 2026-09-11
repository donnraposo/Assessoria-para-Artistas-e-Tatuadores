from django.db import models


class ReceiptStatus(models.TextChoices):
    CONFIRMED = "CONFIRMED", "Confirmed"
