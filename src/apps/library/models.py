from django.conf import settings
from django.contrib.auth import get_user_model
from django.db import models
from django.utils import timezone
from django.utils.translation import gettext_lazy as _
from django_lifecycle import LifecycleModel, hook
from django_lifecycle.hooks import AFTER_CREATE, BEFORE_SAVE

from common.model import BaseModel

User = get_user_model()


class Author(BaseModel):
    name = models.CharField(max_length=255, verbose_name=_("Name"))
    bio = models.TextField(verbose_name=_("Biography"), blank=True)

    class Meta:
        verbose_name = _("Author")
        verbose_name_plural = _("Authors")

    def __str__(self):
        return self.name


class Book(BaseModel):
    title = models.CharField(max_length=255, verbose_name=_("Title"))
    description = models.TextField(verbose_name=_("Description"), blank=True)
    is_available = models.BooleanField(verbose_name=_("Is Available"), default=True)
    author = models.ForeignKey(
        Author,
        on_delete=models.SET_NULL,
        null=True,
        blank=True,
        related_name="books",
        verbose_name=_("Author"),
    )

    class Meta:
        verbose_name = _("Book")
        verbose_name_plural = _("Books")

    def __str__(self) -> str:
        return self.title


class Borrow(BaseModel, LifecycleModel):
    user = models.ForeignKey(
        User,
        on_delete=models.CASCADE,
        related_name="borrows",
        verbose_name=_("User"),
    )
    book = models.ForeignKey(
        Book,
        on_delete=models.CASCADE,
        related_name="borrows",
        verbose_name=_("Book"),
    )
    borrow_date = models.DateField(verbose_name=_("Borrow Date"), auto_now_add=True)
    due_date = models.DateField(verbose_name=_("Due Date"))
    return_date = models.DateField(verbose_name=_("Return Date"), null=True, blank=True)

    class Meta:
        verbose_name = _("Borrow")
        verbose_name_plural = _("Borrows")
        constraints = [
            models.UniqueConstraint(
                name="unique_book_per_user", fields=["user", "book", "created_at"]
            )
        ]

    @hook(BEFORE_SAVE)
    def set_due_date(self: "Borrow"):
        self.due_date = timezone.now() + timezone.timedelta(
            days=settings.DUE_DATE_PERIOD_DAY
        )

    @hook(AFTER_CREATE)
    def mark_book_as_unavailable(self: "Borrow") -> None:
        book: Book = self.book
        if book.is_available:
            book.is_available = False
            book.save(update_fields=["is_available"])

    def __str__(self) -> str:
        return f"{self.user} borrowed {self.book} on {self.borrow_date}"


class Notification(BaseModel):
    borrow = models.ForeignKey(
        Borrow,
        on_delete=models.CASCADE,
        related_name="notifications",
        verbose_name=_("Borrow"),
    )
    message = models.TextField(verbose_name=_("Message"))
    is_delivered = models.BooleanField(verbose_name=_("Is Delivered"), default=True)
    is_seen = models.BooleanField(verbose_name=_("Is Seen"), default=False)

    class Meta:
        verbose_name = _("Notification")
        verbose_name_plural = _("Notifications")
