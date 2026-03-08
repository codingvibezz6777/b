from django.db.models.signals import post_save
from django.dispatch import receiver
from django.conf import settings
from .models import Booking
from django.template.loader import render_to_string
import resend

# Initialize Resend
resend.api_key = settings.RESEND_API_KEY



@receiver(post_save, sender=Booking)
def send_booking_emails(sender, instance, created, **kwargs):
    if not created:
        return

    try:
        # ---------- Admin Notification ----------
        admin_html = render_to_string("booking_notification.html", {
            "booking": instance,
        })
        
        resend.Emails.send({
            "from": "Booking App <admin@star-bookings.com>",
            "to": [settings.ADMIN_EMAIL],
            "subject": f"New Booking for {instance.celebrity.name}",
            "html": admin_html
        })

        # ---------- User Confirmation ----------
        user_html = render_to_string("booking_cornfirmation_user.html", {
            "booking": instance,
        })
        
        resend.Emails.send({
            "from": "Booking App <admin@star-bookings.com>",
            "to": [instance.email],
            "subject": f"Booking Confirmation - {instance.celebrity.name}",
            "html": user_html
        })

    except Exception as e:
        print("Email sending failed:", e)