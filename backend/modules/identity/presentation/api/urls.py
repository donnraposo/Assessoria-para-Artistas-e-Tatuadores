from django.urls import path

from .views.csrf_token_view import CsrfTokenView
from .views.current_user_view import CurrentUserView
from .views.login_view import LoginView
from .views.logout_view import LogoutView
from .views.password_reset_confirm_view import PasswordResetConfirmView
from .views.password_reset_request_view import PasswordResetRequestView
from .views.register_view import RegisterView

urlpatterns = [
    path("csrf/", CsrfTokenView.as_view(), name="csrf-token"),
    path("register/", RegisterView.as_view(), name="register"),
    path("login/", LoginView.as_view(), name="login"),
    path("logout/", LogoutView.as_view(), name="logout"),
    path("me/", CurrentUserView.as_view(), name="current-user"),
    path("password/request/", PasswordResetRequestView.as_view(), name="password-reset-request"),
    path("password/confirm/", PasswordResetConfirmView.as_view(), name="password-reset-confirm"),
]
