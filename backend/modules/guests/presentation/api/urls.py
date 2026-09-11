from django.urls import path

from .views.guest_proposal_collection_view import GuestProposalCollectionView
from .views.guest_proposal_confirm_view import GuestProposalConfirmView
from .views.guest_proposal_ready_view import GuestProposalReadyView
from .views.guest_transition_view import GuestTransitionView

urlpatterns = [
    path("proposals/", GuestProposalCollectionView.as_view(), name="guest-proposal-list"),
    path(
        "proposals/<uuid:proposal_id>/ready/",
        GuestProposalReadyView.as_view(),
        name="guest-proposal-ready",
    ),
    path(
        "proposals/<uuid:proposal_id>/confirm/",
        GuestProposalConfirmView.as_view(),
        name="guest-proposal-confirm",
    ),
    path("<uuid:guest_id>/transition/", GuestTransitionView.as_view(), name="guest-transition"),
]
