from django.urls import path

from .views.booking_confirm_view import BookingConfirmView
from .views.booking_external_response_view import BookingExternalResponseView
from .views.booking_payment_status_view import BookingPaymentStatusView
from .views.booking_request_create_view import BookingRequestCreateView
from .views.booking_response_view import BookingResponseView
from .views.studio_availability_collection_view import StudioAvailabilityCollectionView
from .views.studio_booking_request_collection_view import StudioBookingRequestCollectionView
from .views.studio_price_collection_view import StudioPriceCollectionView
from .views.studio_profile_view import StudioProfileView
from .views.studio_review_view import StudioReviewView
from .views.studio_submit_view import StudioSubmitView
from .views.workstation_collection_view import WorkstationCollectionView

urlpatterns = [
    path("me/", StudioProfileView.as_view(), name="studio-profile"),
    path("me/submit/", StudioSubmitView.as_view(), name="studio-submit"),
    path("me/workstations/", WorkstationCollectionView.as_view(), name="studio-workstations"),
    path("me/prices/", StudioPriceCollectionView.as_view(), name="studio-prices"),
    path(
        "me/availability/",
        StudioAvailabilityCollectionView.as_view(),
        name="studio-availability",
    ),
    path(
        "me/booking-requests/",
        StudioBookingRequestCollectionView.as_view(),
        name="studio-booking-request-list",
    ),
    path("<uuid:studio_id>/review/", StudioReviewView.as_view(), name="studio-review"),
    path("booking-requests/", BookingRequestCreateView.as_view(), name="booking-request-create"),
    path(
        "booking-requests/<uuid:request_id>/respond/",
        BookingResponseView.as_view(),
        name="booking-response",
    ),
    path(
        "booking-requests/<uuid:request_id>/external-response/",
        BookingExternalResponseView.as_view(),
        name="booking-external-response",
    ),
    path(
        "booking-requests/<uuid:request_id>/confirm/",
        BookingConfirmView.as_view(),
        name="booking-confirm",
    ),
    path(
        "bookings/<uuid:booking_id>/payment/",
        BookingPaymentStatusView.as_view(),
        name="booking-payment-status",
    ),
]
