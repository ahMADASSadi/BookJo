from apps.library.models import Author, Book, Borrow, User


class LibraryRepository:
    book = Book.objects
    borrow = Borrow.objects
    author = Author.objects

    @classmethod
    def get_books(cls):
        return cls.book.filter(is_available=True)

    @classmethod
    def get_authors(cls):
        return cls.author.all()

    @classmethod
    def get_borrows(cls, user: User, active: bool = True):
        return cls.borrow.filter(user=user, deleted_at__isnull=active).all()
