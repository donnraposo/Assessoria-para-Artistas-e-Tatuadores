import pytest

from modules.identity.infrastructure.persistence.models import User


@pytest.mark.django_db
def test_user_email_is_normalized() -> None:
    user = User.objects.create_user(
        email="ARTIST@EXAMPLE.COM",
        password="strong-pass",
        full_name="Artist",
    )

    assert user.email == "artist@example.com"
