from rest_framework import generics, status
from rest_framework.response import Response
from .models import Borrow, Book
from .serializers import BorrowSerializer, ReturnBookSerializer, BookSerializer
from rest_framework.exceptions import ValidationError
from .permissions import IsAdminRole, IsMemberRole, IsAdminOrMember
from rest_framework.viewsets import ModelViewSet
from rest_framework.permissions import SAFE_METHODS

class BookViewSet(ModelViewSet):
    queryset = Book.objects.all()
    serializer_class = BookSerializer

    def get_permissions(self):
        if self.action in ['create', 'update', 'partial_update', 'destroy']:
            # Only admins can create, update, or delete books
            permission_classes = [IsAdminRole]
        elif self.action in ['list', 'retrieve']:
            # Both members and admins can view books
            permission_classes = [IsAdminRole | IsMemberRole]  # Combine logic for viewing
        else:
            # Default permission classes
            permission_classes = []
        return [permission() for permission in permission_classes]

class AdminBorrowListView(generics.ListAPIView):
    queryset = Borrow.objects.all()
    serializer_class = BorrowSerializer
    permission_classes = [IsAdminRole]

class BorrowBookView(generics.GenericAPIView):
    serializer_class = BorrowSerializer
    permission_classes = [IsMemberRole]

    def get(self, request, *args, **kwargs):
        user = request.user
        borrow_records = Borrow.objects.filter(user=user, return_date__isnull=True)
        data = BorrowSerializer(borrow_records, many=True).data
        return Response(data)

    def post(self, request, *args, **kwargs):
        serializer = self.get_serializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        self.perform_create(serializer)
        return Response(serializer.data, status=status.HTTP_201_CREATED)

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

class ReturnBookView(generics.UpdateAPIView):
    queryset = Borrow.objects.all()
    serializer_class = ReturnBookSerializer
    permission_classes = [IsMemberRole]

    def get_queryset(self):
        """Limit queryset to only the borrow records of the logged-in user."""
        user = self.request.user
        return Borrow.objects.filter(user=user, return_date__isnull=True)
