from django.urls import path
from .views import BorrowBookView, ReturnBookView, BookViewSet, AdminBorrowListView

urlpatterns = [
    # Explicitly map actions of the BookViewSet
    path('books/', BookViewSet.as_view({'get': 'list', 'post': 'create'}), name='book-list-create'),
    path('books/<int:pk>/', BookViewSet.as_view({'get': 'retrieve', 'put': 'update', 'delete': 'destroy'}), name='book-detail'),

    # Endpoints for borrowing and returning books
    path('borrow/', BorrowBookView.as_view(), name='borrow-book'),
    path('all-borrowed-list/', AdminBorrowListView.as_view(), name='all-borrowed-book'),
    path('return/<int:pk>/', ReturnBookView.as_view(), name='return-book'),
]