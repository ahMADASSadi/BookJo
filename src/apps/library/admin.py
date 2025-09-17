from django.contrib import admin

from apps.library.models import Author, Book, Borrow, Notification


@admin.register(Author)
class AuthorAdmin(admin.ModelAdmin):
    list_display = ["name", "bio"]
    search_fields = ("name",)


@admin.register(Book)
class BookAdmin(admin.ModelAdmin):
    list_display = ["title", "author", "is_available"]
    list_filter = ["is_available", "author"]
    search_fields = ["title", "author__name"]


@admin.register(Borrow)
class BorrowAdmin(admin.ModelAdmin):
    list_display = ["user", "book", "borrow_date", "return_date"]
    list_filter = ["borrow_date", "return_date", "book", "user"]
    search_fields = ["user__username", "book__title"]


@admin.register(Notification)
class NotificationAdmin(admin.ModelAdmin):
    list_display = ["borrow", "is_seen", "message"]
