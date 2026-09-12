from django.db import models


class StudioPaymentStatus(models.TextChoices):
    """RN-033: the Artist pays the Studio outside the platform."""

    PENDING = "PENDING", "Pending"
    PAID = "PAID", "Paid"
