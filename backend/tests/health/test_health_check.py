import pytest
from django.urls import reverse
from rest_framework.test import APIClient


@pytest.mark.django_db
def test_health_check_returns_ok(api_client: APIClient) -> None:
    response = api_client.get(reverse("health-check"))

    assert response.status_code == 200
    assert response.json() == {"status": "ok"}


@pytest.mark.django_db
def test_readiness_check_validates_database(api_client: APIClient) -> None:
    response = api_client.get(reverse("readiness-check"))

    assert response.status_code == 200
    assert response.json() == {"status": "ready", "database": "available"}


@pytest.fixture
def api_client() -> APIClient:
    return APIClient()
