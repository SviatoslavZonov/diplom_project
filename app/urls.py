from django.urls import path, include
from rest_framework.routers import DefaultRouter
from .views import (
    LoginView,
    RegisterView,
    ProductViewSet,
    CartViewSet,
    ContactViewSet,
    OrderViewSet,
    OrderHistoryView
)

app_name = 'app'

router = DefaultRouter()

# Регистрируем ViewSets
router.register(r'products', ProductViewSet, basename='product')
router.register(r'cart', CartViewSet, basename='cart')
router.register(r'contacts', ContactViewSet, basename='contact')
router.register(r'orders', OrderViewSet, basename='order')

urlpatterns = [
    # Эндпоинты аутентификации
    path('api/auth/register/', RegisterView.as_view(), name='register'),
    path('api/auth/login/', LoginView.as_view(), name='login'),
    
    # Эндпоинты для заказов
    path('api/orders/history/', OrderHistoryView.as_view(), name='order-history'),
    
    # Подключаем все зарегистрированные ViewSets
    path('api/', include(router.urls)),
]
