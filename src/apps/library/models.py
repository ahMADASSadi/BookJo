from django.contrib.auth import get_user_model
from django.db import models
from django.utils.translation import gettext_lazy as _
from django_lifecycle import LifecycleModel, hook
from django_lifecycle.hooks import AFTER_CREATE

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
    borrow_date = models.DateField(verbose_name=_("Borrow Date"), auto_now=True)
    return_date = models.DateField(verbose_name=_("Return Date"), null=True, blank=True)

    class Meta:
        verbose_name = _("Borrow")
        verbose_name_plural = _("Borrows")
        constraints = [
            models.UniqueConstraint(
                name="unique_book_per_user", fields=["user", "book"]
            )
        ]

    @hook(AFTER_CREATE)
    def set_return_date(self: "Borrow") -> None:
        book: Book = self.book
        if book.is_available:
            book.is_available = False
            book.save(update_fields=["is_available"])

    def __str__(self) -> str:
        return f"{self.user} borrowed {self.book} on {self.borrow_date}"
