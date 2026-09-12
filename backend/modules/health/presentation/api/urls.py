from django.urls import path

from .health_check_view import HealthCheckView
from .readiness_check_view import ReadinessCheckView

urlpatterns = [
    path("health/", HealthCheckView.as_view(), name="health-check"),
    path("ready/", ReadinessCheckView.as_view(), name="readiness-check"),
]
