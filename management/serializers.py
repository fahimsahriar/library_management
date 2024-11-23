from datetime import datetime
from rest_framework import serializers
from .models import Borrow, Book
from rest_framework.exceptions import ValidationError
from django.utils.timezone import now

class BookSerializer(serializers.ModelSerializer):
    class Meta:
        model = Book
        fields = '__all__'

class BorrowSerializer(serializers.ModelSerializer):
    book = serializers.PrimaryKeyRelatedField(queryset=Book.objects.all())

    class Meta:
        model = Borrow
        fields = ['book', 'user', 'borrow_date', 'return_date', 'deadline', 'fine']

class ReturnBookSerializer(serializers.ModelSerializer):
    book = serializers.PrimaryKeyRelatedField(queryset=Book.objects.all(), read_only=False)

    class Meta:
        model = Borrow
        fields = ['id', 'book', 'borrow_date', 'return_date', 'deadline', 'fine']

    def validate(self, attrs):
        """Validate that the borrow instance exists for the user before returning."""
        request = self.context.get('request')
        if request and request.method == 'PUT':  # Check only on return (update)
            user = request.user
            borrow_instance = Borrow.objects.filter(user=user, book=attrs.get('book'), return_date__isnull=True).first()
            if not borrow_instance:
                raise ValidationError("You haven't borrowed this book or it's already returned.")
        return attrs

    def update(self, instance, validated_data):
        """Handle the return of a book."""
        # Calculate overdue fine if the deadline has passed
        current_date = now()
        if instance.deadline and current_date > instance.deadline:
            overdue_days = (current_date - instance.deadline).days
            fine_amount = overdue_days * 5  # Assuming 5 BDT per day
            instance.fine = fine_amount

            # Update the user's credit and ban status
            user = instance.user
            if fine_amount > 0:
                if user.credit >= fine_amount:
                    user.credit -= fine_amount
                else:
                    user.credit = 0
                    user.is_banned = True  # Mark user as banned if credit is exhausted

            # Update user's total fine for record-keeping
            user.total_fine += fine_amount
            user.save()

        # Mark the return date and update book availability
        instance.return_date = current_date
        instance.book.is_available = True
        instance.book.save()

        # Save the updated borrow instance
        instance.save()
        return instance
