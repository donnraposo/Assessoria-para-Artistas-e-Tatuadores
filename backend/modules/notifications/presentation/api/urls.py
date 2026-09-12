from django.urls import path

from .views.notification_collection_view import NotificationCollectionView
from .views.notification_read_view import NotificationReadView

urlpatterns = [
    path("", NotificationCollectionView.as_view(), name="notification-list"),
    path("<uuid:notification_id>/read/", NotificationReadView.as_view(), name="notification-read"),
]
