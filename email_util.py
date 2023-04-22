import os
import smtplib
from email.message import EmailMessage


def send_email(subject, content, to):
    message = EmailMessage()
    message.set_content(content)
    message["Subject"] = subject
    message["From"] = os.environ["EMAIL_USERNAME"]
    message["To"] = to

    with smtplib.SMTP(os.environ["EMAIL_HOST"], os.environ["EMAIL_PORT"]) as server:
        server.login(os.environ["EMAIL_USERNAME"], os.environ["EMAIL_PASSWORD"])
        server.send_message(message)
