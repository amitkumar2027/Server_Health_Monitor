from .email_alert import send_email
from .telegram_alert import send_telegram


def send_alert(subject, message):
    send_email(subject, message)
    send_telegram(f"{subject}\n{message}")
