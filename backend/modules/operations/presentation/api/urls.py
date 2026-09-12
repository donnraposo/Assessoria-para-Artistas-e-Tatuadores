from django.urls import path

from .views.operations_dashboard_view import OperationsDashboardView
from .views.operations_queue_view import OperationsQueueView
from .views.operations_reference_view import OperationsReferenceView
from .views.role_workspace_view import RoleWorkspaceView

urlpatterns = [
    path("dashboard/", OperationsDashboardView.as_view(), name="operations-dashboard"),
    path("queues/<str:queue_name>/", OperationsQueueView.as_view(), name="operations-queue"),
    path("workspace/", RoleWorkspaceView.as_view(), name="role-workspace"),
    path("reference-data/", OperationsReferenceView.as_view(), name="operations-reference"),
]
