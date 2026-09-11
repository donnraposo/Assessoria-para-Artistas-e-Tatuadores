from rest_framework.permissions import BasePermission

from modules.identity.domain.enums import RoleType


class HasArtistRole(BasePermission):
    def has_permission(self, request, view) -> bool:
        return (
            request.user.is_authenticated
            and request.user.roles.filter(role__code=RoleType.ARTIST).exists()
        )
