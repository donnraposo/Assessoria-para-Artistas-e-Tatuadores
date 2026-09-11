from django.conf import settings
from django.contrib.auth.tokens import default_token_generator
from django.core.mail import send_mail
from django.utils.encoding import force_bytes
from django.utils.http import urlsafe_base64_decode, urlsafe_base64_encode

from modules.identity.infrastructure.persistence.models import User


class PasswordResetService:
    @staticmethod
    def request(email: str) -> None:
        user = User.objects.filter(email=email.strip().lower(), is_active=True).first()
        if user is None:
            return
        uid = urlsafe_base64_encode(force_bytes(user.pk))
        token = default_token_generator.make_token(user)
        url = f"{settings.FRONTEND_PASSWORD_RESET_URL}?uid={uid}&token={token}"
        send_mail(
            subject="Reset your password",
            message=f"Use this link to reset your password: {url}",
            from_email=settings.DEFAULT_FROM_EMAIL,
            recipient_list=[user.email],
        )

    @staticmethod
    def confirm(uid: str, token: str, password: str) -> bool:
        try:
            user_id = urlsafe_base64_decode(uid).decode()
            user = User.objects.get(pk=user_id, is_active=True)
        except (ValueError, TypeError, OverflowError, User.DoesNotExist):
            return False
        if not default_token_generator.check_token(user, token):
            return False
        user.set_password(password)
        user.save(update_fields=["password", "updated_at"])
        return True
