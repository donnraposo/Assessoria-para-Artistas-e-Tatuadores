import uuid

from django.db import models

from modules.guests.domain.enums import GuestStatus


class Guest(models.Model):
    id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)
    proposal = models.OneToOneField("guests.GuestProposal", on_delete=models.PROTECT)
    artist = models.ForeignKey("artists.ArtistProfile", on_delete=models.PROTECT)
    city = models.CharField(max_length=120)
    country_code = models.CharField(max_length=2)
    starts_on = models.DateField()
    ends_on = models.DateField()
    timezone = models.CharField(max_length=64)
    currency = models.CharField(max_length=3)
    status = models.CharField(
        max_length=20, choices=GuestStatus.choices, default=GuestStatus.CAPTURING
    )
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    class Meta:
        db_table = "guests_guest"
        ordering = ["-starts_on"]

    def __str__(self) -> str:
        return f"{self.artist}:{self.city}:{self.starts_on}"
