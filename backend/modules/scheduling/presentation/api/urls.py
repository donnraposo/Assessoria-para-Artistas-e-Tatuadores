from django.urls import path

from .views.appointment_collection_view import AppointmentCollectionView
from .views.cancellation_decision_view import CancellationDecisionView
from .views.cancellation_request_create_view import CancellationRequestCreateView
from .views.guest_occupancy_view import GuestOccupancyView

urlpatterns = [
    path("appointments/", AppointmentCollectionView.as_view(), name="appointment-list"),
    path(
        "appointments/<uuid:appointment_id>/cancellation-requests/",
        CancellationRequestCreateView.as_view(),
        name="appointment-cancellation-request",
    ),
    path(
        "cancellation-requests/<uuid:cancellation_id>/decide/",
        CancellationDecisionView.as_view(),
        name="cancellation-decision",
    ),
    path(
        "guests/<uuid:guest_id>/occupancy/",
        GuestOccupancyView.as_view(),
        name="guest-occupancy",
    ),
]
