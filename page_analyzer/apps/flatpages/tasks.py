from django.core.mail import send_mail
from django.template.loader import render_to_string

from taskapp.celery import app


@app.task(name='send_email')
def send_admin_request_notification(subject, text, from_email, recipient_list, **kwargs):
    template = 'flatpages/admin_notification_contact_us.html'
    context = {
        'description': text,
        'email': from_email
    }
    html_message = render_to_string(template, context)

    send_mail(
        subject=subject, message=text, from_email=from_email,
        recipient_list=recipient_list, html_message=html_message
    )
