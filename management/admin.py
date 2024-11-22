from django.contrib import admin
from .models import Book

@admin.register(Book)
class BookAdmin(admin.ModelAdmin):
    list_display = ('title', 'author', 'is_available', 'created_at', 'updated_at')
    search_fields = ('title', 'author')
    list_filter = ('is_available',)
