from django.contrib import admin
from .models import Book
from .models import Borrow

@admin.register(Book)
class BookAdmin(admin.ModelAdmin):
    list_display = ('title', 'author', 'is_available', 'created_at', 'updated_at')
    search_fields = ('title', 'author')
    list_filter = ('is_available',)

@admin.register(Borrow)
class BorrowAdmin(admin.ModelAdmin):
    list_display = ('user', 'book', 'borrow_date', 'return_date', 'deadline', 'fine')
    search_fields = ('user__username', 'book__title')
    list_filter = ('borrow_date', 'return_date')