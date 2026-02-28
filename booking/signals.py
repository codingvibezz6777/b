from django.db.models.signals import post_save
from django.dispatch import receiver
from django.core.mail import EmailMultiAlternatives
from django.template.loader import render_to_string
from django.conf import settings
from .models import Booking

@receiver(post_save, sender=Booking)
def send_booking_emails(sender, instance, created, **kwargs):
    if created:
        # Admin Email
        subject_admin = f"New Booking for {instance.celebrity.name}"
        html_admin = render_to_string('booking_notification.html', {'booking': instance})
        admin_msg = EmailMultiAlternatives(subject_admin, '', settings.DEFAULT_FROM_EMAIL, ['youradminemail@example.com'])
        admin_msg.attach_alternative(html_admin, "text/html")
        admin_msg.send(fail_silently=False)

        #  User Confirmation Email
        subject_user = f"Booking Confirmation - {instance.celebrity.name}"
        html_user = render_to_string('booking_confirmation_user.html', {'booking': instance})
        user_msg = EmailMultiAlternatives(subject_user, '', settings.DEFAULT_FROM_EMAIL, [instance.email])
        user_msg.attach_alternative(html_user, "text/html")
        user_msg.send(fail_silently=False)