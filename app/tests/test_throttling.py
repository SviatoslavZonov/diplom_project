# Тест троттлинга
from django.test import override_settings
from django.core.cache import cache
from rest_framework.test import APITestCase
from rest_framework import status
from django.urls import reverse


class ThrottlingTests(APITestCase):
    def setUp(self):
        cache.clear()  # Очистка кэша перед каждым тестом

    def test_anon_throttle(self):
        url = reverse('app:product-list')
        for i in range(4):
            response = self.client.get(url)
            if response.status_code == status.HTTP_429_TOO_MANY_REQUESTS:
                break
        self.assertEqual(response.status_code, status.HTTP_429_TOO_MANY_REQUESTS)

    def test_user_throttle(self):
    # Регистрация (проверяем статус)
        register_response = self.client.post(
            reverse('app:register'),
            {
                "email": "test@example.com",
                "password": "SecurePass123!",
                "first_name": "Test",
                "last_name": "User"
            }, 
            format='json'
        )
        self.assertEqual(register_response.status_code, status.HTTP_201_CREATED)

        # Авторизация (проверяем статус и наличие токена)
        auth_response = self.client.post(
            reverse('app:token_obtain_pair'),
            {"email": "test@example.com", "password": "SecurePass123!"},
            format='json'
        )
        self.assertEqual(auth_response.status_code, status.HTTP_200_OK)
        self.assertIn('access', auth_response.data)  # Добавим проверку

        token = auth_response.data['access']
        self.client.credentials(HTTP_AUTHORIZATION=f'Bearer {token}')
        
        url = reverse('app:product-list')
        for i in range(6):
            response = self.client.get(url)
            if response.status_code == status.HTTP_429_TOO_MANY_REQUESTS:
                break
        self.assertEqual(response.status_code, status.HTTP_429_TOO_MANY_REQUESTS)