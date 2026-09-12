from django.db import models


class MyTripStatus(models.TextChoices):
    EMPTY = "EMPTY", "Empty"
    PENDING = "PENDING", "Pending"
    UPDATED = "UPDATED", "Updated"
    UNAVAILABLE = "UNAVAILABLE", "Unavailable"
