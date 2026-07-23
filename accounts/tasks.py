from celery import shared_task
from django.core.mail import send_mail
from django.conf import settings



@shared_task
def send_email_task(confirmation_url, user_email):
    subject = "Confirm your new email address"
    message = (
        f"Please confirm your new email address by clicking this link:\n\n"
        f"{confirmation_url}"
    )
    return send_mail(subject, message, settings.DEFAULT_FROM_EMAIL, [user_email]) 