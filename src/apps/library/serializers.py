from django.db import DatabaseError
from rest_framework.exceptions import ValidationError
from rest_framework.serializers import ModelSerializer, PrimaryKeyRelatedField

from apps.library.models import Author, Book, Borrow


class AuthorSerializer(ModelSerializer):
    class Meta:
        model = Author
        fields = ["id", "name", "bio", "created_at", "updated_at"]


class AuthorListSerializer(ModelSerializer):
    class Meta:
        model = Author
        fields = ["id", "name", "bio"]

    def create(self, validated_data):
        try:
            return super().create(validated_data)
        except (ValidationError, DatabaseError) as e:
            raise ValidationError({"detail": str(e)})

    def update(self, instance, validated_data):
        try:
            for attr, value in validated_data.items():
                setattr(instance, attr, value)
            return super().update(instance, validated_data)
        except (ValidationError, DatabaseError) as e:
            raise ValidationError({"detail": str(e)})


class BookListSerializer(ModelSerializer):
    class Meta:
        model = Book
        fields = [
            "id",
            "title",
            "is_available",
        ]


class BookCreateSerializer(ModelSerializer):
    class Meta:
        model = Book
        fields = [
            "title",
            "description",
            "author",
        ]

    def create(self, validated_data):
        try:
            return super().create(validated_data)
        except (ValidationError, DatabaseError) as e:
            raise ValidationError({"detail": str(e)})


class BookUpdateSerializer(ModelSerializer):
    class Meta:
        model = Book
        fields = [
            "title",
            "is_available",
            "description",
            "author",
        ]

    def update(self, instance, validated_data):
        try:
            for attr, value in validated_data.items():
                setattr(instance, attr, value)
            instance.save()
            return super().update(instance, validated_data)
        except (ValidationError, DatabaseError) as e:
            raise ValidationError({"detail": str(e)})


class BookDetailSerializer(ModelSerializer):
    author = AuthorListSerializer(read_only=True)

    class Meta:
        model = Book
        fields = [
            "id",
            "title",
            "is_available",
            "description",
            "author",
            "created_at",
            "updated_at",
        ]


class BorrowCreateSerializer(ModelSerializer):
    book_id = PrimaryKeyRelatedField(
        queryset=Book.objects.filter(is_available=True), source="book", write_only=True
    )

    class Meta:
        model = Borrow
        fields = ["book_id"]

    def create(self, validated_data):
        validated_data["user"] = self.context.get("user")
        return super().create(validated_data)


class BorrowUpdateSerializer(ModelSerializer):
    class Meta:
        model = Borrow
        fields = ["id"]


class BorrowSerializer(ModelSerializer):
    book = BookDetailSerializer(read_only=True)

    class Meta:
        model = Borrow
        fields = ["id", "book", "return_date", "borrow_date"]


class BorrowListSerializer(ModelSerializer):
    book = BookListSerializer(read_only=True)

    class Meta:
        model = Borrow
        fields = ["id", "book", "return_date"]
