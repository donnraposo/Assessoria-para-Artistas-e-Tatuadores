from django.urls import path

from .views.booking_confirm_view import BookingConfirmView
from .views.booking_request_create_view import BookingRequestCreateView
from .views.booking_response_view import BookingResponseView
from .views.studio_booking_request_collection_view import StudioBookingRequestCollectionView
from .views.studio_profile_view import StudioProfileView
from .views.studio_review_view import StudioReviewView
from .views.studio_submit_view import StudioSubmitView

urlpatterns = [
    path("me/", StudioProfileView.as_view(), name="studio-profile"),
    path("me/submit/", StudioSubmitView.as_view(), name="studio-submit"),
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
        "booking-requests/<uuid:request_id>/confirm/",
        BookingConfirmView.as_view(),
        name="booking-confirm",
    ),
]
