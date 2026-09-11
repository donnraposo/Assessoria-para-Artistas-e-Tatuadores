import uuid

from django.db import models

from modules.identity.domain.enums import RoleType


class Role(models.Model):
    id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)
    code = models.CharField(max_length=24, choices=RoleType.choices, unique=True)
    name = models.CharField(max_length=80)

    class Meta:
        db_table = "identity_role"
        ordering = ["name"]

    def __str__(self) -> str:
        return self.name
