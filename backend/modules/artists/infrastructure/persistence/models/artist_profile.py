import uuid

from django.conf import settings
from django.core.validators import MinValueValidator
from django.db import models


class ArtistProfile(models.Model):
    id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)
    user = models.OneToOneField(settings.AUTH_USER_MODEL, on_delete=models.CASCADE)
    professional_name = models.CharField(max_length=160)
    biography = models.TextField(blank=True)
    years_experience = models.PositiveSmallIntegerField(default=0)
    styles = models.JSONField(default=list)
    currency = models.CharField(max_length=3, default="BRL")
    minimum_tattoo_value = models.DecimalField(
        max_digits=12,
        decimal_places=2,
        validators=[MinValueValidator(0)],
    )
    expected_ticket = models.DecimalField(
        max_digits=12,
        decimal_places=2,
        validators=[MinValueValidator(0)],
    )
    daily_session_value = models.DecimalField(
        max_digits=12,
        decimal_places=2,
        null=True,
        blank=True,
        validators=[MinValueValidator(0)],
    )
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    class Meta:
        db_table = "artists_profile"

    def __str__(self) -> str:
        return self.professional_name
