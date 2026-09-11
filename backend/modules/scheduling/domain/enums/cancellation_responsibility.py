from django.db import models


class CancellationResponsibility(models.TextChoices):
    ARTIST = "ARTIST", "Artist"
