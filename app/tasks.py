from celery import shared_task
from django.core.mail import send_mail
from django.conf import settings
from app.management.commands.import_products import Command

@shared_task(name="send_email")
def send_email(subject, message, recipient_list):
    send_mail(
        subject,
        message,
        settings.DEFAULT_FROM_EMAIL,
        recipient_list,
        fail_silently=False,
    )

@shared_task(name="do_import")
def do_import(path):
    Command().handle(path=path)