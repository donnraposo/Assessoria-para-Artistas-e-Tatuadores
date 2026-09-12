from django.urls import path

from .views.artist_application_detail_view import ArtistApplicationDetailView
from .views.artist_application_review_view import ArtistApplicationReviewView
from .views.artist_application_view import ArtistApplicationView
from .views.artist_profile_view import ArtistProfileView
from .views.availability_collection_view import AvailabilityCollectionView
from .views.availability_override_view import AvailabilityOverrideView
from .views.portfolio_collection_view import PortfolioCollectionView

urlpatterns = [
    path("me/", ArtistProfileView.as_view(), name="artist-profile"),
    path("me/application/", ArtistApplicationView.as_view(), name="artist-application"),
    path("me/portfolio/", PortfolioCollectionView.as_view(), name="artist-portfolio"),
    path("me/availability/", AvailabilityCollectionView.as_view(), name="artist-availability"),
    path(
        "availability/<uuid:availability_id>/override/",
        AvailabilityOverrideView.as_view(),
        name="artist-availability-override",
    ),
    path(
        "applications/<uuid:application_id>/",
        ArtistApplicationDetailView.as_view(),
        name="artist-application-detail",
    ),
    path(
        "applications/<uuid:application_id>/review/",
        ArtistApplicationReviewView.as_view(),
        name="artist-application-review",
    ),
]
