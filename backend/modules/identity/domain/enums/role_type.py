from django.db import models


class RoleType(models.TextChoices):
    ARTIST = "ARTIST", "Artist"
    STUDIO = "STUDIO", "Studio"
    ADVISORY = "ADVISORY", "Advisory"
