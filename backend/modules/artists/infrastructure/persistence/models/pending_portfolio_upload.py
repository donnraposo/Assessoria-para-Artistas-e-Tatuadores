import uuid

from django.db import models


class PendingPortfolioUpload(models.Model):
    id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)
    artist = models.ForeignKey("artists.ArtistProfile", on_delete=models.CASCADE)
    object_key = models.CharField(max_length=500, unique=True)
    original_name = models.CharField(max_length=255)
    content_type = models.CharField(max_length=100)
    size_bytes = models.PositiveBigIntegerField()
    caption = models.CharField(max_length=300, blank=True)
    style = models.CharField(max_length=80, blank=True)
    position = models.PositiveSmallIntegerField(default=0)
    expires_at = models.DateTimeField()
    confirmed_at = models.DateTimeField(null=True, blank=True)
    created_at = models.DateTimeField(auto_now_add=True)

    class Meta:
        db_table = "artists_pending_portfolio_upload"
        ordering = ["-created_at"]

    def __str__(self) -> str:
        return self.original_name
