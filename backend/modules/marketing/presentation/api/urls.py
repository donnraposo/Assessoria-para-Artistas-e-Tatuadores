from django.urls import path

from .views.campaign_collection_view import CampaignCollectionView
from .views.campaign_spend_view import CampaignSpendView
from .views.guest_metrics_view import GuestMetricsView

urlpatterns = [
    path("campaigns/", CampaignCollectionView.as_view(), name="campaign-list"),
    path(
        "campaigns/<uuid:campaign_id>/spend/",
        CampaignSpendView.as_view(),
        name="campaign-spend",
    ),
    path("guests/<uuid:guest_id>/metrics/", GuestMetricsView.as_view(), name="guest-metrics"),
]
