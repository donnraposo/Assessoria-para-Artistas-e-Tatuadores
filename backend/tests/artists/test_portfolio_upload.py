from decimal import Decimal
from unittest.mock import patch

import pytest
from rest_framework.test import APIClient

from modules.artists.infrastructure.persistence.models import ArtistProfile, PortfolioItem
from modules.identity.domain.enums import RoleType
from modules.identity.infrastructure.persistence.models import Role, User, UserRole


def create_artist(email: str) -> User:
    user = User.objects.create_user(email=email, full_name="Portfolio Artist")
    role, _ = Role.objects.get_or_create(code=RoleType.ARTIST, defaults={"name": "Artist"})
    UserRole.objects.create(user=user, role=role)
    ArtistProfile.objects.create(
        user=user,
        professional_name="Portfolio Ink",
        minimum_tattoo_value=Decimal("500.00"),
        expected_ticket=Decimal("900.00"),
    )
    return user


@pytest.mark.django_db
@patch(
    "modules.artists.infrastructure.storage.portfolio_storage.PortfolioStorage.create_download_url",
    return_value="http://storage.local/read",
)
@patch(
    "modules.artists.application.services.portfolio_upload_service.PortfolioStorage.delete",
)
@patch(
    "modules.artists.application.services.portfolio_upload_service.PortfolioStorage.inspect",
    return_value=(8, "image/jpeg", b"\xff\xd8\xffimage"),
)
@patch(
    "modules.artists.application.services.portfolio_upload_service.PortfolioStorage.create_upload_url",
    return_value="http://storage.local/upload",
)
def test_artist_completes_private_portfolio_lifecycle(
    create_url,
    inspect_object,
    delete_object,
    download_url,
) -> None:
    artist = create_artist("portfolio@example.com")
    other_artist = create_artist("other-portfolio@example.com")
    client = APIClient()
    client.force_authenticate(artist)

    request_response = client.post(
        "/api/v1/artists/me/portfolio/uploads/",
        {
            "original_name": "blackwork.jpg",
            "content_type": "image/jpeg",
            "size_bytes": 8,
            "caption": "Blackwork study",
            "style": "Blackwork",
            "position": 0,
        },
        format="json",
    )
    upload_id = request_response.data["upload_id"]
    confirm_response = client.post(
        f"/api/v1/artists/me/portfolio/uploads/{upload_id}/confirm/",
        {},
        format="json",
    )
    item_id = confirm_response.data["id"]
    list_response = client.get("/api/v1/artists/me/portfolio/")
    access_response = client.get(f"/api/v1/artists/me/portfolio/{item_id}/access/")

    client.force_authenticate(other_artist)
    forbidden_response = client.get(f"/api/v1/artists/me/portfolio/{item_id}/access/")
    client.force_authenticate(artist)
    delete_response = client.delete(f"/api/v1/artists/me/portfolio/{item_id}/")

    assert request_response.status_code == 201
    assert request_response.data["upload_url"] == "http://storage.local/upload"
    assert "object_key" not in request_response.data
    assert confirm_response.status_code == 200
    assert "object_key" not in confirm_response.data
    assert len(list_response.data) == 1
    assert access_response.data["access_url"] == "http://storage.local/read"
    assert forbidden_response.status_code == 404
    assert delete_response.status_code == 204
    assert not PortfolioItem.objects.filter(pk=item_id).exists()
    create_url.assert_called_once()
    inspect_object.assert_called_once()
    download_url.assert_called_once()
    delete_object.assert_called_once()


@pytest.mark.django_db
@patch(
    "modules.artists.application.services.portfolio_upload_service.PortfolioStorage.inspect",
    return_value=(8, "image/jpeg", b"notimage"),
)
@patch(
    "modules.artists.application.services.portfolio_upload_service.PortfolioStorage.create_upload_url",
    return_value="http://storage.local/upload",
)
def test_portfolio_confirmation_rejects_invalid_file_content(create_url, inspect_object) -> None:
    artist = create_artist("invalid-portfolio@example.com")
    client = APIClient()
    client.force_authenticate(artist)
    request_response = client.post(
        "/api/v1/artists/me/portfolio/uploads/",
        {
            "original_name": "fake.jpg",
            "content_type": "image/jpeg",
            "size_bytes": 8,
        },
        format="json",
    )

    response = client.post(
        f"/api/v1/artists/me/portfolio/uploads/{request_response.data['upload_id']}/confirm/",
        {},
        format="json",
    )

    assert response.status_code == 409
    assert "supported image" in response.data["detail"]
    assert PortfolioItem.objects.count() == 0
    create_url.assert_called_once()
    inspect_object.assert_called_once()
