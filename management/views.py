from rest_framework.permissions import IsAdminUser, IsAuthenticated
from rest_framework import generics, status
from rest_framework.response import Response
from .models import Borrow, Book
from .serializers import BorrowSerializer, ReturnBookSerializer, BookSerializer
from rest_framework.exceptions import ValidationError

class BookListCreateView(generics.ListCreateAPIView):
    queryset = Book.objects.all()
    serializer_class = BookSerializer
    permission_classes = [IsAuthenticated]

class BorrowBookView(generics.CreateAPIView):
    serializer_class = BorrowSerializer
    permission_classes = [IsAuthenticated]

    def perform_create(self, serializer):
        user = self.request.user
        book = serializer.validated_data['book']

        # Check if the user has exceeded the borrow limit
        if Borrow.objects.filter(user=user, return_date__isnull=True).count() >= 5:
            raise ValidationError("You have reached the borrow limit of 5 books.")

        # Check if the book is available
        if not book.is_available:
            raise ValidationError("This book is currently not available.")

        # Update the book availability and save the borrow record
        book.is_available = False
        book.save()

        # Save the borrow record and set the user automatically
        serializer.save(user=user)

class UserBorrowedBooksView(generics.ListAPIView):
    serializer_class = BorrowSerializer
    permission_classes = [IsAuthenticated]

    def get_queryset(self):
        user = self.request.user
        return Borrow.objects.filter(user=user, return_date__isnull=True)

class ReturnBookView(generics.UpdateAPIView):
    queryset = Borrow.objects.all()
    serializer_class = ReturnBookSerializer
    permission_classes = [IsAuthenticated]

    def get_queryset(self):
        """Limit queryset to only the borrow records of the logged-in user."""
        user = self.request.user
        return Borrow.objects.filter(user=user, return_date__isnull=True)
