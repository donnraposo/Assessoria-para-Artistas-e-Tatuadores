import uuid

from django.db import models

from modules.studios.domain.enums import StudioPaymentStatus


class StudioBooking(models.Model):
    id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)
    request = models.OneToOneField("studios.StudioBookingRequest", on_delete=models.PROTECT)
    confirmed_by = models.ForeignKey("identity.User", on_delete=models.PROTECT)
    payment_status = models.CharField(
        max_length=12,
        choices=StudioPaymentStatus.choices,
        default=StudioPaymentStatus.PENDING,
    )
    confirmed_at = models.DateTimeField(auto_now_add=True)

    class Meta:
        db_table = "studios_booking"

    def __str__(self) -> str:
        return str(self.id)
