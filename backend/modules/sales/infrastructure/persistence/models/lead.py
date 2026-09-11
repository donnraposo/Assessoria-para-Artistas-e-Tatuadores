import uuid

from django.conf import settings
from django.db import models

from modules.sales.domain.enums import LeadStatus


class Lead(models.Model):
    id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)
    guest = models.ForeignKey("guests.Guest", on_delete=models.PROTECT, related_name="leads")
    external_reference = models.CharField(max_length=160, blank=True)
    source = models.CharField(max_length=80)
    client_name = models.CharField(max_length=160)
    client_email = models.EmailField(blank=True)
    client_phone = models.CharField(max_length=40, blank=True)
    notes = models.TextField(blank=True)
    status = models.CharField(max_length=12, choices=LeadStatus.choices, default=LeadStatus.OPEN)
    created_by = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.PROTECT)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    class Meta:
        db_table = "sales_lead"
        ordering = ["-created_at"]
        constraints = [
            models.UniqueConstraint(
                fields=["guest", "external_reference"],
                condition=~models.Q(external_reference=""),
                name="uq_lead_guest_external_reference",
            )
        ]

    def __str__(self) -> str:
        return f"{self.client_name}:{self.guest_id}"
