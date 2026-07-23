from django.conf import settings
from django.utils.encoding import force_bytes
from django.utils.http import urlsafe_base64_encode
from .tokens import email_change_token_generator


def build_email_change_confirmation_link(user):
    uid = urlsafe_base64_encode(force_bytes(user.pk))
    token = email_change_token_generator.make_token(user)
    return (
        f"{settings.EMAIL_FRONTEND_PROTOCOL}://{settings.DOMAIN}"
        f"/email-change-confirm/"
        f"?uid={uid}&token={token}"
    )