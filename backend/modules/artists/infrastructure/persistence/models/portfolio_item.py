import uuid

from django.core.validators import MinValueValidator
from django.db import models


class PortfolioItem(models.Model):
    id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)
    artist = models.ForeignKey("artists.ArtistProfile", on_delete=models.CASCADE)
    object_key = models.CharField(max_length=500, unique=True)
    original_name = models.CharField(max_length=255)
    content_type = models.CharField(max_length=100)
    size_bytes = models.PositiveBigIntegerField(validators=[MinValueValidator(1)])
    caption = models.CharField(max_length=300, blank=True)
    style = models.CharField(max_length=80, blank=True)
    position = models.PositiveSmallIntegerField(default=0)
    created_at = models.DateTimeField(auto_now_add=True)

    class Meta:
        db_table = "artists_portfolio_item"
        ordering = ["position", "created_at"]

    def __str__(self) -> str:
        return self.original_name
