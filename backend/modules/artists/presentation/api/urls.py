from django.urls import path

from .views.artist_application_review_view import ArtistApplicationReviewView
from .views.artist_application_view import ArtistApplicationView
from .views.artist_profile_view import ArtistProfileView
from .views.availability_collection_view import AvailabilityCollectionView
from .views.portfolio_collection_view import PortfolioCollectionView
from .views.portfolio_item_access_view import PortfolioItemAccessView
from .views.portfolio_item_detail_view import PortfolioItemDetailView
from .views.portfolio_upload_confirm_view import PortfolioUploadConfirmView
from .views.portfolio_upload_request_view import PortfolioUploadRequestView

urlpatterns = [
    path("me/", ArtistProfileView.as_view(), name="artist-profile"),
    path("me/application/", ArtistApplicationView.as_view(), name="artist-application"),
    path("me/portfolio/", PortfolioCollectionView.as_view(), name="artist-portfolio"),
    path(
        "me/portfolio/uploads/",
        PortfolioUploadRequestView.as_view(),
        name="artist-portfolio-upload-request",
    ),
    path(
        "me/portfolio/uploads/<uuid:upload_id>/confirm/",
        PortfolioUploadConfirmView.as_view(),
        name="artist-portfolio-upload-confirm",
    ),
    path(
        "me/portfolio/<uuid:item_id>/access/",
        PortfolioItemAccessView.as_view(),
        name="artist-portfolio-item-access",
    ),
    path(
        "me/portfolio/<uuid:item_id>/",
        PortfolioItemDetailView.as_view(),
        name="artist-portfolio-item-detail",
    ),
    path("me/availability/", AvailabilityCollectionView.as_view(), name="artist-availability"),
    path(
        "applications/<uuid:application_id>/review/",
        ArtistApplicationReviewView.as_view(),
        name="artist-application-review",
    ),
]
