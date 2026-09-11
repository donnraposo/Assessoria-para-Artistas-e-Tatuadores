import uuid

from django.db import models


class Workstation(models.Model):
    id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)
    studio = models.ForeignKey(
        "studios.Studio",
        on_delete=models.CASCADE,
        related_name="workstations",
    )
    name = models.CharField(max_length=80)
    is_active = models.BooleanField(default=True)

    class Meta:
        db_table = "studios_workstation"
        constraints = [models.UniqueConstraint(fields=["studio", "name"], name="uq_studio_station")]

    def __str__(self) -> str:
        return f"{self.studio}:{self.name}"
