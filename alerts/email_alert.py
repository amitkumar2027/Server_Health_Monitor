import smtplib
from email.mime.text import MIMEText
from config.settings import EMAIL_SENDER, EMAIL_PASSWORD, EMAIL_RECEIVER


def send_email(subject, message):

    try:
        msg = MIMEText(message)
        msg['Subject'] = subject
        msg['From'] = EMAIL_SENDER
        msg['To'] = EMAIL_RECEIVER

        server = smtplib.SMTP("smtp.gmail.com", 587)
        server.starttls()
        server.login(EMAIL_SENDER, EMAIL_PASSWORD)
        server.send_message(msg)
        server.quit()

    except Exception as e:
        print("Email error:", e)
