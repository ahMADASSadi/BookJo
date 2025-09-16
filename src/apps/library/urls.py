from rest_framework.routers import DefaultRouter

from apps.library.views import AuthorViewSet, BookViewSet, BorrowViewSet

router = DefaultRouter()

router.register("books/available", BookViewSet, basename="books")
router.register("authors", AuthorViewSet, basename="authors")
router.register("borrows", BorrowViewSet, basename="borrows")

urlpatterns = router.urls
