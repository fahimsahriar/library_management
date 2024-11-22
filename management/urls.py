from django.urls import path
from .views import BorrowBookView, ReturnBookView, BookListCreateView, UserBorrowedBooksView

urlpatterns = [
    path('books/', BookListCreateView.as_view(), name='book-list-create'),
    path('borrow/', BorrowBookView.as_view(), name='borrow-book'),
    path('borrowed/', UserBorrowedBooksView.as_view(), name='user-borrowed-books'),
    path('return/<int:pk>/', ReturnBookView.as_view(), name='return-book'),
]
