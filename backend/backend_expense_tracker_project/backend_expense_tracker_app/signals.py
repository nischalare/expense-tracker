from django.db.models.signals import post_save
from django.dispatch import receiver
from django.contrib.auth.models import User
from django.core.mail import send_mail
import logging
from backend_expense_tracker_app.models import Expense, Profile  # ✅ Correct model imports

logger = logging.getLogger(__name__)  # ✅ Setup logging


@receiver(post_save, sender=User)
def create_user_profile(sender, instance, created, **kwargs):
    """Automatically create a Profile when a user registers"""
    if created:
        Profile.objects.create(user=instance)
        logger.info(f"✅ Profile created for new user: {instance.username}")


@receiver(post_save, sender=User)
def save_user_profile(sender, instance, **kwargs):
    """Save Profile when user updates info"""
    if hasattr(instance, "profile"):
        instance.profile.save()
        logger.info(f"✅ Profile updated for user: {instance.username}")
    else:
        logger.warning(f"⚠️ User {instance.username} has no profile!")


@receiver(post_save, sender=Expense)  # ✅ Attach to Expense Model, not User
def notify_large_expense(sender, instance, created, **kwargs):
    """Sends an alert when a user records an expense above the limit"""
    EXPENSE_LIMIT = 500.00

    if created and instance.amount > EXPENSE_LIMIT:  # ✅ Check only new expenses
        alert_msg = f"⚠️ Expense Alert: {instance.user.username} recorded an expense of ${instance.amount}!"
        print(alert_msg)
        logger.warning(alert_msg)

        # ✅ Send Email Notification
        send_mail(
            subject="Expense Alert",
            message=f"Hi {instance.user.username}, you have recorded a high expense of ${instance.amount}.",
            from_email="admin@expensetracker.com",
            recipient_list=[instance.user.email],
            fail_silently=True,
        )


