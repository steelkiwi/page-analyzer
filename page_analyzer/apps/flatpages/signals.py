from django.conf import settings
from django.db.models.signals import post_save
from django.dispatch import receiver

from flatpages.models import ContactUsRequest
from flatpages.tasks import send_admin_request_notification


@receiver(post_save, sender=ContactUsRequest, dispatch_uid='contact_us_post_save')
def contact_us_post_save(sender, instance, **kwargs):
    send_admin_request_notification.delay(
        f'Received request from {instance.email}',
        instance.description,
        instance.email,
        [settings.DEFAULT_FROM_EMAIL, ],
    )
