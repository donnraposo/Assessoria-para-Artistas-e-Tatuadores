import pytest
from rest_framework.request import Request
from rest_framework.test import APIRequestFactory

from modules.identity.domain.enums import RoleType
from modules.identity.infrastructure.persistence.models import Role, User, UserRole
from modules.identity.presentation.api.permissions import (
    HasAdvisoryRole,
    HasArtistRole,
    HasStudioRole,
)


@pytest.mark.django_db
@pytest.mark.parametrize(
    ("role_code", "permission_type"),
    [
        (RoleType.ADVISORY, HasAdvisoryRole),
        (RoleType.ARTIST, HasArtistRole),
        (RoleType.STUDIO, HasStudioRole),
    ],
)
def test_role_permission_accepts_only_matching_role(role_code, permission_type) -> None:
    user = User.objects.create_user(email=f"{role_code}@example.com", full_name="User")
    role = Role.objects.create(code=role_code, name=role_code.label)
    UserRole.objects.create(user=user, role=role)
    request = Request(APIRequestFactory().get("/"))
    request.user = user

    assert permission_type().has_permission(request, None)
