from django.db import models
from django.conf import settings
from datetime import timedelta
from django.utils.timezone import now

def default_deadline():
    return now() + timedelta(days=14)

class Book(models.Model):
    title = models.CharField(max_length=255)
    author = models.CharField(max_length=255)
    is_available = models.BooleanField(default=True)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    def __str__(self):
        return self.title



class Borrow(models.Model):
    user = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE)
    book = models.ForeignKey('Book', on_delete=models.CASCADE)
    borrow_date = models.DateTimeField(auto_now_add=True)
    return_date = models.DateTimeField(null=True, blank=True)
    deadline = models.DateTimeField(default=default_deadline)
    fine = models.DecimalField(max_digits=10, decimal_places=2, default=0)

    def calculate_fine(self):
        if self.return_date and self.return_date > self.deadline:
            overdue_days = (self.return_date - self.deadline).days
            return max(overdue_days * 5, 0)  # 5 BDT per day
        return 0

    def save(self, *args, **kwargs):
        self.fine = self.calculate_fine()
        super().save(*args, **kwargs)

    def __str__(self):
        return f"{self.user.username} borrowed {self.book.title}"

