from django.contrib.auth import get_user_model
from rest_framework import serializers
from management.models import Borrow
from .models import CustomUser

User = get_user_model()

class UserRegistrationSerializer(serializers.ModelSerializer):
    class Meta:
        model = CustomUser
        fields = ['username', 'password', 'role', 'email']
        extra_kwargs = {
            'password': {'write_only': True},
            'role': {'required': False},
        }

    def create(self, validated_data):
        # Default to member if role is not specified
        role = validated_data.get('role', 'member')

        # If the role is 'admin', ensure only an authenticated admin can create it
        request = self.context.get('request')
        if role == 'admin':
            if not request or not request.user.is_authenticated:
                raise serializers.ValidationError("Authentication is required to create an admin user.")
            if request.user.role != 'admin':
                raise serializers.ValidationError("Only admins can create other admin users.")

        # Create user and set password
        user = CustomUser.objects.create(
            username=validated_data['username'],
            email=validated_data.get('email'),
            role=role
        )
        user.set_password(validated_data['password'])
        user.save()
        return user

class MemberSerializer(serializers.ModelSerializer):
    class Meta:
        model = CustomUser
        fields = ['id', 'username', 'email', 'total_fine', 'credit', 'is_banned']

class BorrowSerializer(serializers.ModelSerializer):
    class Meta:
        model = Borrow
        fields = ['book', 'borrow_date', 'return_date']

class UserDetailSerializer(serializers.ModelSerializer):
    current_borrowed_books = serializers.SerializerMethodField()
    borrowing_history = serializers.SerializerMethodField()

    class Meta:
        model = CustomUser
        fields = ['id', 'username', 'email', 'role', 'total_fine', 'credit', 'is_banned', 'current_borrowed_books', 'borrowing_history']

    def get_current_borrowed_books(self, obj):
        # Filter books currently borrowed and not yet returned
        borrowed_books = Borrow.objects.filter(user=obj, return_date__isnull=True)
        return BorrowSerializer(borrowed_books, many=True).data

    def get_borrowing_history(self, obj):
        # Include all borrow records (both returned and unreturned)
        borrow_history = Borrow.objects.filter(user=obj)
        return BorrowSerializer(borrow_history, many=True).data
