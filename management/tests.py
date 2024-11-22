from rest_framework.test import APITestCase
from rest_framework import status
from django.contrib.auth import get_user_model
from .models import Book

class BookAPITest(APITestCase):
    def setUp(self):
        # Create an admin user
        self.admin_user = get_user_model().objects.create_user(
            username='admin',
            password='adminpass',
            role='admin'
        )
        self.client.login(username='admin', password='adminpass')

        # Create a sample book
        self.book = Book.objects.create(
            title="Django Testing",
            author="Test Author",
            is_available=True
        )

    def test_get_books(self):
        # Authenticate the client
        self.client.force_authenticate(user=self.admin_user)

        # Test GET request
        response = self.client.get('/api/management/books/')
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertIn("Django Testing", response.data[0]["title"])
