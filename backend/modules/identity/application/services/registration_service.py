from django.db import transaction

from modules.audit.infrastructure.persistence.models import AuditEvent
from modules.identity.domain.enums import RoleType
from modules.identity.infrastructure.persistence.models import Role, User, UserRole

SELF_SERVICE_ROLES = {
    RoleType.ARTIST: "Artist",
    RoleType.STUDIO: "Studio",
}


class RegistrationService:
    @staticmethod
    @transaction.atomic
    def register(*, email: str, password: str, full_name: str, role_code: str) -> User:
        if role_code not in SELF_SERVICE_ROLES:
            raise ValueError("This role cannot be self-registered.")
        user = User.objects.create_user(email=email, password=password, full_name=full_name)
        role, _ = Role.objects.get_or_create(
            code=role_code,
            defaults={"name": SELF_SERVICE_ROLES[role_code]},
        )
        UserRole.objects.create(user=user, role=role)
        AuditEvent.objects.create(
            actor=user,
            action="user.registered",
            resource_type="User",
            resource_id=str(user.id),
            changes={"role": role_code},
        )
        return user
