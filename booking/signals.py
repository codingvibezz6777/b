from django.db.models.signals import post_save
from django.dispatch import receiver
from django.conf import settings
from .models import Booking
import resend

# Initialize Resend
resend.api_key = settings.RESEND_API_KEY


@receiver(post_save, sender=Booking)
def send_booking_emails(sender, instance, created, **kwargs):
    if not created:
        return

    try:
        # ---------- Admin Notification ----------
        resend.Emails.send({
            "from": "Booking App <starbookingofficial@gmail.com>",
            "to": [settings.ADMIN_EMAIL],
            "subject": f"New Booking for {instance.celebrity.name}",
            "html": f"""
                <h2>New Booking Received</h2>
                <p><strong>Celebrity:</strong> {instance.celebrity.name}</p>
                <p><strong>User Email:</strong> {instance.email}</p>
            """
        })

        # ---------- User Confirmation ----------
        resend.Emails.send({
            "from": "Booking App <starbookingofficial@gmail.com>",
            "to": [instance.email],
            "subject": f"Booking Confirmation - {instance.celebrity.name}",
            "html": f"""
                <h2>Booking Confirmed ✅</h2>
                <p>Hello, your booking for <strong>{instance.celebrity.name}</strong> was successful.</p>
                <p>We will contact you soon.</p>
            """
        })

    except Exception as e:
        print("Email sending failed:", e)