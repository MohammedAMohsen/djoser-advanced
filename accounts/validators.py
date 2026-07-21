from datetime import date
from rest_framework import serializers


RESERVED_USERNAMES = {
    "admin",
    "administrator",
    "root",
    "superuser",
    "system",
    "support",
}


BLOCKED_EMAIL_DOMAINS = {
    "mailinator.com",
    "10minutemail.com",
    "tempmail.com",
}


def validate_username(value):
    if value.lower() in RESERVED_USERNAMES:
        raise serializers.ValidationError("This username is reserved.")
    return value.lower()


def validate_email(value):
    domain = value.split("@")[-1].lower()
    if domain in BLOCKED_EMAIL_DOMAINS:
        raise serializers.ValidationError("Temporary email addresses are not allowed.")
    return value.lower()


def validate_birth_date(value):
    today = date.today()
    age = (
        today.year 
        - value.year
        - ((today.month, today.day) < (value.month, value.day))
    )
    if age < 18:
        raise serializers.ValidationError("You must be at least 18 years old.")
    return value