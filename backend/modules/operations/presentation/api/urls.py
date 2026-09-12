from django.urls import path

from .views.operations_dashboard_view import OperationsDashboardView
from .views.operations_queue_view import OperationsQueueView
from .views.role_workspace_view import RoleWorkspaceView

urlpatterns = [
    path("dashboard/", OperationsDashboardView.as_view(), name="operations-dashboard"),
    path("queues/<str:queue_name>/", OperationsQueueView.as_view(), name="operations-queue"),
    path("workspace/", RoleWorkspaceView.as_view(), name="role-workspace"),
]
