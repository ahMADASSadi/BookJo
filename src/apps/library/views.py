from django.utils import timezone
from rest_framework.decorators import action
from rest_framework.permissions import IsAuthenticated
from rest_framework.viewsets import ModelViewSet

from apps.library.repository import LibraryRepository
from apps.library.schemas import (
    borrow_schema,
    extend_schema,
    extend_schema_view,
    my_borrows_schema,
    return_book_schema,
)
from apps.library.serializers import (
    AuthorListSerializer,
    AuthorSerializer,
    BookCreateSerializer,
    BookDetailSerializer,
    BookListSerializer,
    BookUpdateSerializer,
    BorrowCreateSerializer,
    BorrowListSerializer,
    BorrowSerializer,
    BorrowUpdateSerializer,
)
from common.responses import APIResponse
from common.view import ViewSetMixin


@extend_schema(tags=["Books"])
class BookViewSet(ViewSetMixin, ModelViewSet):
    """
    API endpoint for managing books in the library.

    Provides CRUD operations for books, including listing, retrieving, creating, and updating book records.
    """

    action_serializer_class = {
        "retrieve": BookDetailSerializer,
        "list": BookListSerializer,
        "create": BookCreateSerializer,
        "update": BookUpdateSerializer,
        "partial_update": BookUpdateSerializer,
    }
    default_serializer_class = BookListSerializer
    _repo = LibraryRepository

    def get_queryset(self):
        return self._repo.get_books()


@extend_schema(tags=["Authors"])
class AuthorViewSet(ViewSetMixin, ModelViewSet):
    action_serializer_class = {"retrieve": AuthorSerializer, "delete": AuthorSerializer}
    default_serializer_class = AuthorListSerializer
    _repo = LibraryRepository

    def get_queryset(self):
        return self._repo.get_authors()


@extend_schema(tags=["Borrows"])
@extend_schema_view(**borrow_schema)
class BorrowViewSet(ViewSetMixin, ModelViewSet):
    permission_classes = [IsAuthenticated]
    action_serializer_class = {
        "list": BorrowListSerializer,
        "create": BorrowCreateSerializer,
        "update": BorrowUpdateSerializer,
        "my": BorrowSerializer,
        "return_book": BorrowSerializer,
    }
    default_serializer_class = BorrowSerializer
    _repo = LibraryRepository

    def get_queryset(self):
        user = self.get_user()
        active_param = self.request.query_params.get("active", None)
        if active_param is None or active_param.lower() in ("true", "1", "yes"):
            return self._repo.get_borrows(user=user, active=True)
        else:
            return self._repo.get_borrows(user=user, active=False)

    @extend_schema(**return_book_schema)
    @action(methods=["put"], detail=True, url_path="return")
    def return_book(self, request, *args, **kwargs):
        borrow = self.get_object()
        book = borrow.book
        if not book.is_available:
            book.is_available = True
            book.save()
        borrow.return_date = timezone.now()
        serializer = self.get_serializer(borrow)
        self.destroy(request)
        return APIResponse.success(data=serializer.data)

    @extend_schema(**my_borrows_schema)
    @action(methods=["get"], detail=False, url_path="my")
    def my(self, request, *args, **kwargs):
        queryset = self.get_queryset()
        serializer = self.get_serializer(queryset, many=True)
        return APIResponse.success(data=serializer.data)
