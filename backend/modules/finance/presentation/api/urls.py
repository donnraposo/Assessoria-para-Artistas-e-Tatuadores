from django.urls import path

from .views.financial_entry_confirm_view import FinancialEntryConfirmView
from .views.guest_finance_summary_view import GuestFinanceSummaryView

urlpatterns = [
    path(
        "guests/<uuid:guest_id>/summary/",
        GuestFinanceSummaryView.as_view(),
        name="guest-finance-summary",
    ),
    path(
        "entries/<uuid:entry_id>/confirm/",
        FinancialEntryConfirmView.as_view(),
        name="financial-entry-confirm",
    ),
]
