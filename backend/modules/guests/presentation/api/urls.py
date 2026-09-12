from django.urls import path

from .views.guest_collection_view import GuestCollectionView
from .views.guest_proposal_collection_view import GuestProposalCollectionView
from .views.guest_proposal_confirm_view import GuestProposalConfirmView
from .views.guest_proposal_ready_view import GuestProposalReadyView
from .views.guest_proposal_transition_view import GuestProposalTransitionView
from .views.guest_studio_collection_view import GuestStudioCollectionView
from .views.guest_transition_view import GuestTransitionView

urlpatterns = [
    path("", GuestCollectionView.as_view(), name="guest-list"),
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
    path(
        "proposals/<uuid:proposal_id>/transition/",
        GuestProposalTransitionView.as_view(),
        name="guest-proposal-transition",
    ),
    path("<uuid:guest_id>/transition/", GuestTransitionView.as_view(), name="guest-transition"),
    path(
        "<uuid:guest_id>/studios/",
        GuestStudioCollectionView.as_view(),
        name="guest-studio-list",
    ),
]
