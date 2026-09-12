from django.urls import path

from .views.accommodation_collection_view import AccommodationCollectionView
from .views.accommodation_detail_view import AccommodationDetailView
from .views.my_trip_view import MyTripView
from .views.travel_segment_collection_view import TravelSegmentCollectionView
from .views.travel_segment_detail_view import TravelSegmentDetailView

urlpatterns = [
    path(
        "guests/<uuid:guest_id>/travel-segments/",
        TravelSegmentCollectionView.as_view(),
        name="travel-segment-list",
    ),
    path(
        "travel-segments/<uuid:segment_id>/",
        TravelSegmentDetailView.as_view(),
        name="travel-segment-detail",
    ),
    path(
        "guests/<uuid:guest_id>/accommodations/",
        AccommodationCollectionView.as_view(),
        name="accommodation-list",
    ),
    path(
        "accommodations/<uuid:accommodation_id>/",
        AccommodationDetailView.as_view(),
        name="accommodation-detail",
    ),
    path("guests/<uuid:guest_id>/my-trip/", MyTripView.as_view(), name="my-trip"),
]
