from django.core.mail import send_mail

from Sprint.settings import EMAIL_HOST_USER
from SprintLib.queue import MessagingSupport


class Command(MessagingSupport):
    help = "starts file email sender"
    queue_name = "email"

    def process(self, payload: dict):
        subject = payload['subject']
        message = payload['message']
        email = payload['email']
        send_mail(
            subject,
            message,
            EMAIL_HOST_USER,
            [email]
        )
