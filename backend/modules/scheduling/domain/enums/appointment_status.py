from django.db import models


class AppointmentStatus(models.TextChoices):
    PENDING_PAYMENT = "PENDING_PAYMENT", "Pending payment"
    CONFIRMED = "CONFIRMED", "Confirmed"
    CANCELLATION_REQUESTED = "CANCELLATION_REQUESTED", "Cancellation requested"
    CANCELLED = "CANCELLED", "Cancelled"
    COMPLETED = "COMPLETED", "Completed"
