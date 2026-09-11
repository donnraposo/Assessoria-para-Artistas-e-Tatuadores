import uuid

from django.core.validators import MinValueValidator
from django.db import models

from modules.guests.domain.enums import ProposalStatus


class GuestProposal(models.Model):
    id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)
    artist = models.ForeignKey("artists.ArtistProfile", on_delete=models.PROTECT)
    primary_studio = models.ForeignKey("studios.Studio", on_delete=models.PROTECT)
    city = models.CharField(max_length=120)
    country_code = models.CharField(max_length=2)
    starts_on = models.DateField()
    ends_on = models.DateField()
    timezone = models.CharField(max_length=64)
    currency = models.CharField(max_length=3)
    ads_budget = models.DecimalField(
        max_digits=12, decimal_places=2, validators=[MinValueValidator(0)]
    )
    minimum_tattoo_value = models.DecimalField(
        max_digits=12, decimal_places=2, validators=[MinValueValidator(0)]
    )
    expected_ticket = models.DecimalField(
        max_digits=12, decimal_places=2, validators=[MinValueValidator(0)]
    )
    daily_session_value = models.DecimalField(
        max_digits=12, decimal_places=2, null=True, blank=True
    )
    status = models.CharField(
        max_length=20, choices=ProposalStatus.choices, default=ProposalStatus.DRAFT
    )
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    class Meta:
        db_table = "guests_proposal"
        ordering = ["-created_at"]

    def __str__(self) -> str:
        return f"{self.artist}:{self.city}:{self.starts_on}"
