from django.contrib import admin
from django.urls import include, path

urlpatterns = [
    path("admin/", admin.site.urls),
    path("api/v1/auth/", include("modules.identity.presentation.api.urls")),
    path("api/v1/artists/", include("modules.artists.presentation.api.urls")),
    path("api/v1/studios/", include("modules.studios.presentation.api.urls")),
    path("api/v1/guests/", include("modules.guests.presentation.api.urls")),
    path("api/v1/schedule/", include("modules.scheduling.presentation.api.urls")),
    path("api/v1/sales/", include("modules.sales.presentation.api.urls")),
    path("api/v1/marketing/", include("modules.marketing.presentation.api.urls")),
    path("api/v1/finance/", include("modules.finance.presentation.api.urls")),
    path("api/v1/logistics/", include("modules.logistics.presentation.api.urls")),
    path("api/v1/notifications/", include("modules.notifications.presentation.api.urls")),
    path("api/v1/operations/", include("modules.operations.presentation.api.urls")),
    path("api/v1/", include("modules.health.presentation.api.urls")),
]
