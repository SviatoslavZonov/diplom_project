from django.urls import reverse
from rest_framework.test import APITestCase
from rest_framework import status
from django.contrib.auth import get_user_model
from app.models import Product, Supplier, Cart, Contact, Order
import time
from unittest.mock import patch
from django.core.cache import cache
from django.test import override_settings

User = get_user_model()

@override_settings(
    REST_FRAMEWORK={
        'DEFAULT_THROTTLE_RATES': {
            'anon': '1000/minute',  # Временно увеличить лимит, чтобы не было конфликтов с тестом троттлинга
            'user': '1000/minute',
        }
    }
)

class AuthTests(APITestCase):
    def tearDown(self):
        cache.clear()  # Очистка кэша Redis

    @patch('app.tasks.send_email.delay')
    def test_register(self, mock_send_email):
        url = reverse('app:register')
        data = {
            'email': 'test@example.com',
            'password': 'testpassword123',
            'first_name': 'Test',
            'last_name': 'User'
        }
        response = self.client.post(url, data, format='json')
        self.assertEqual(response.status_code, status.HTTP_201_CREATED)
        self.assertTrue(User.objects.filter(email='test@example.com').exists())

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
        self.supplier = Supplier.objects.create(name="Test Supplier")
        self.product = Product.objects.create(
            name="Test Product",
            supplier=self.supplier,
            price=100.00,
            quantity=10
        )

    def test_list_products(self):
        url = reverse('app:product-list')
        response = self.client.get(url)
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        
        # Если пагинация включена:
        if 'results' in response.data:
            self.assertEqual(len(response.data['results']), 1)
        else:
            # Если пагинация отключена:
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
        self.assertEqual(response.data['product']['id'], self.product.id)

class OrderViewSetTests(APITestCase):
    def setUp(self):
        self.user = User.objects.create_user(email="user@example.com", password="password123")
        self.client.force_authenticate(user=self.user)
        self.contact = Contact.objects.create(
            user=self.user,
            first_name="Petr",
            last_name="petrov",
            email="ppetr@example.com",
            phone="1234567890",
            city="Test City"
        )
        self.product = Product.objects.create(
            name="Test Product",
            supplier=Supplier.objects.create(name="Test Supplier"),
            price=100.00,
            quantity=5
        )
        self.cart = Cart.objects.create(
            user=self.user,
            product=self.product,
            quantity=2
        )

    def test_order_creation(self):
        url = reverse('app:order-list')
        response = self.client.post(url, {"contact": self.contact.id})
        self.assertEqual(response.status_code, status.HTTP_201_CREATED)
        self.assertEqual(Order.objects.count(), 1)
    
    def test_order_creation(self):
        url = reverse('app:order-list')
        response = self.client.post(
            url, 
            {"contact": self.contact.id}, 
            format='json'  # Добавлено
        )
        self.assertEqual(response.status_code, status.HTTP_201_CREATED)

    @patch('app.tasks.send_email.delay')  # Мокируем Celery-задачу
    @patch('app.views.send_mail')  # Мокируем отправку email
    def test_email_send_failure(self, mock_send, mock_celery):
        mock_send.side_effect = Exception("SMTP error")
        url = reverse('app:order-list')
        response = self.client.post(
            url, 
            {"contact": self.contact.id}, 
            format='json'
        )
        self.assertEqual(response.status_code, status.HTTP_201_CREATED)
        # Проверка логов (опционально):
        # self.assertLogs(logger='app.views', level='ERROR')