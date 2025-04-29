from django.urls import reverse
from rest_framework.test import APITestCase
from rest_framework import status
from django.contrib.auth import get_user_model
from app.models import Product, Supplier, Cart, Contact, Order
import time

from unittest.mock import patch
from app.tasks import send_email

User = get_user_model()

class AuthTests(APITestCase):
    @patch('app.tasks.send_email.delay')
    def test_register(self, mock_send_email):
        data = {
            'email': 'test@example.com',
            'password': 'testpassword123',
            'first_name': 'Test',
            'last_name': 'User'
        }
        response = self.client.post('/auth/register/', data)
        self.assertEqual(response.status_code, 201)
        mock_send_email.assert_called_once()
    def test_login(self):
        User.objects.create_user(email="test@example.com", password="SecurePass123!")
        url = reverse("app:token_obtain_pair")
        data = {
            "email": "test@example.com",
            "password": "SecurePass123!"
        }
        response = self.client.post(url, data, format="json")
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertIn("access", response.data)

class ProductViewSetTests(APITestCase):
    def setUp(self):
        supplier = Supplier.objects.create(name="Test Supplier")
        Product.objects.create(name="Test Product", price=100, supplier=supplier)

    def test_list_products(self):
        response = self.client.get('/products/')
        self.assertEqual(response.status_code, 200)
        self.assertEqual(len(response.data), 1)

class CartViewSetTests(APITestCase):
    def setUp(self):
        self.user = User.objects.create_user(email="user@example.com", password="password123")
        self.client.force_authenticate(user=self.user)
        self.supplier = Supplier.objects.create(name="Supplier")
        self.product = Product.objects.create(
            name="Product",
            supplier=self.supplier,
            price=50.00,
            quantity=5
        )

    def test_add_to_cart(self):
        url = reverse("app:cart-list")
        data = {
            "product_id": self.product.id,
            "quantity": 2
        }
        response = self.client.post(url, data, format="json")
        self.assertEqual(response.status_code, status.HTTP_201_CREATED)
        self.assertEqual(Cart.objects.count(), 1)