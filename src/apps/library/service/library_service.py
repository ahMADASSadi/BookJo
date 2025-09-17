from django.db import DatabaseError
from django.db.transaction import atomic
from django.utils import timezone

from apps.library.models import Borrow


class LibraryService:
    @classmethod
    def return_book(cls, borrow_instance: "Borrow"):
        with atomic():
            try:
                book = borrow_instance.book
                book.is_available = True
                book.save(update_fields=["is_available"])

                borrow_instance.return_date = timezone.now().date()
                borrow_instance.save(update_fields=["return_date"])

                borrow_instance.notifications.all().delete()
            except Exception:
                raise DatabaseError
