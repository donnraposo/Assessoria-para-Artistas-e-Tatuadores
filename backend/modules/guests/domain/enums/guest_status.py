from django.db import models


class GuestStatus(models.TextChoices):
    CAPTURING = "CAPTURING", "Capturing leads"
    FULLY_BOOKED = "FULLY_BOOKED", "Fully booked"
    IN_PROGRESS = "IN_PROGRESS", "In progress"
    FINISHED = "FINISHED", "Finished"
    CANCELLED = "CANCELLED", "Cancelled"
