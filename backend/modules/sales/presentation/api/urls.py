from django.urls import path

from .views.lead_closing_view import LeadClosingView
from .views.lead_collection_view import LeadCollectionView

urlpatterns = [
    path("leads/", LeadCollectionView.as_view(), name="lead-list"),
    path("leads/<uuid:lead_id>/close/", LeadClosingView.as_view(), name="lead-close"),
]
