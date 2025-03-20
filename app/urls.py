from django.urls import path, include
from rest_framework.routers import DefaultRouter
from app.views import ProductViewSet, OrderViewSet

# Указываем app_name
app_name = 'app'

router = DefaultRouter()
router.register(r'products', ProductViewSet)
router.register(r'orders', OrderViewSet)

urlpatterns = [
    path('', include(router.urls)),
]