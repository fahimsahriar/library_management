from django.contrib.auth import get_user_model
from rest_framework import serializers
from management.models import Borrow

User = get_user_model()

class MemberSerializer(serializers.ModelSerializer):
    class Meta:
        model = User
        fields = ['id', 'username', 'email']


User = get_user_model()

class BorrowSerializer(serializers.ModelSerializer):
    class Meta:
        model = Borrow
        fields = ['book', 'borrow_date', 'return_date']

class UserDetailSerializer(serializers.ModelSerializer):
    current_borrowed_books = serializers.SerializerMethodField()
    borrowing_history = serializers.SerializerMethodField()

    class Meta:
        model = User
        fields = ['id', 'username', 'email', 'role', 'total_fine', 'credit', 'is_banned', 'current_borrowed_books', 'borrowing_history']

    def get_current_borrowed_books(self, obj):
        # Filter books currently borrowed and not yet returned
        borrowed_books = Borrow.objects.filter(user=obj, return_date__isnull=True)
        return BorrowSerializer(borrowed_books, many=True).data

    def get_borrowing_history(self, obj):
        # Include all borrow records (both returned and unreturned)
        borrow_history = Borrow.objects.filter(user=obj)
        return BorrowSerializer(borrow_history, many=True).data
