from celery import shared_task
from django.utils import timezone

from apps.library.models import Borrow, Notification


@shared_task
def check_overdue_books():
    overdue_checkouts = Borrow.objects.filter(
        due_date__lte=timezone.now().date(), return_date__isnull=True
    )

    if not overdue_checkouts:
        return

    notification_count = 0
    for checkout in overdue_checkouts:
        message = f"URGENT: Your checked-out book '{checkout.book.title}' is overdue! Please return it immediately."

        _, created = Notification.objects.get_or_create(
            borrow=checkout,
            defaults={"message": message, "is_delivered": True},
        )
        if created:
            notification_count += 1

    # logger.info(f"Created {notification_count} new overdue book notifications.")


@shared_task
def notify_notifications():
    unseen_notifications = Notification.objects.filter(is_seen=False)

    if not unseen_notifications:
        return

    for notification in unseen_notifications:
        message = f"URGENT: A remider to return the '{notification.borrow.book.title}' book! Please return it immediately."
        print(message)
