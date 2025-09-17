from drf_spectacular.utils import (  # noqa: F401
    OpenApiParameter,
    OpenApiResponse,
    extend_schema,
    extend_schema_view,
)

from apps.library.serializers import (
    BorrowCreateSerializer,
    BorrowListSerializer,
    BorrowSerializer,
    BorrowUpdateSerializer,
)

borrow_schema = {
    "list": extend_schema(
        summary="List borrows",
        description="List all borrows for the authenticated user. Optionally filter by active status with the 'active' query parameter.",
        parameters=[
            OpenApiParameter(
                name="active",
                type=bool,
                location=OpenApiParameter.QUERY,
                required=False,
                description="Filter by active borrows. Accepts true/false, 1/0, yes/no. Defaults to active borrows.",
            ),
        ],
        responses={200: BorrowListSerializer(many=True)},
    ),
    "create": extend_schema(
        summary="Create a borrow",
        description="Create a new borrow record for a book. Only available books can be borrowed.",
        request=BorrowCreateSerializer,
        responses={201: BorrowSerializer},
    ),
    "update": extend_schema(
        summary="Update a borrow",
        description="Update a borrow record.",
        request=BorrowUpdateSerializer,
        responses={200: BorrowSerializer},
    ),
    "partial_update": extend_schema(
        summary="Partially update a borrow",
        description="Partially update a borrow record.",
        request=BorrowUpdateSerializer,
        responses={200: BorrowSerializer},
    ),
    "retrieve": extend_schema(
        summary="Retrieve a borrow",
        description="Retrieve a single borrow record.",
        responses={200: BorrowSerializer},
    ),
    "destroy": extend_schema(
        summary="Delete a borrow",
        description="Delete a borrow record.",
        responses={204: OpenApiResponse(description="No Content")},
    ),
}

return_book_schema = {
    "summary": "Return a borrowed book",
    "description": "Mark a borrowed book as returned. Sets the book as available and records the return date.",
    "responses": {200: {"message": "Success"}},
}
my_borrows_schema = {
    "summary": "List my borrows",
    "description": "List all borrows for the authenticated user.",
    "responses": {200: BorrowSerializer(many=True)},
}
