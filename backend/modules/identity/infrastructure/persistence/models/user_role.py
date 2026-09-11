import uuid

from django.conf import settings
from django.db import models


class UserRole(models.Model):
    id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)
    user = models.ForeignKey(
        settings.AUTH_USER_MODEL,
        on_delete=models.CASCADE,
        related_name="roles",
    )
    role = models.ForeignKey("identity.Role", on_delete=models.PROTECT, related_name="users")
    scope_id = models.UUIDField(null=True, blank=True)
    created_at = models.DateTimeField(auto_now_add=True)

    class Meta:
        db_table = "identity_user_role"
        constraints = [
            models.UniqueConstraint(fields=["user", "role", "scope_id"], name="uq_user_role_scope")
        ]

    def __str__(self) -> str:
        return f"{self.user_id}:{self.role_id}"
