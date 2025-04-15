# Тест тротлинга
from rest_framework.test import APITestCase
from django.urls import reverse

class ThrottlingTests(APITestCase):
    def test_anon_throttle(self):
        url = reverse("app:product-list")
        for _ in range(101):
            response = self.client.get(url)
            if response.status_code == 429:
                break
        self.assertEqual(response.status_code, 429)