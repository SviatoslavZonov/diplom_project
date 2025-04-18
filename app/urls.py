from django.urls import path, include
from rest_framework.routers import DefaultRouter
from rest_framework_simplejwt.views import TokenObtainPairView, TokenRefreshView
from .views import (
    LoginView,
    RegisterView,
    ProductViewSet,
    CartViewSet,
    ContactViewSet,
    OrderViewSet,
    OrderHistoryView
)
from .views import AdminUserViewSet, AdminSupplierViewSet, AdminOrderViewSet

app_name = 'app'

router = DefaultRouter()

# маршруты Администраторов
router.register(r'admin/users', AdminUserViewSet, basename='admin-user')
router.register(r'admin/suppliers', AdminSupplierViewSet, basename='admin-supplier')
router.register(r'admin/orders', AdminOrderViewSet, basename='admin-order')

# Регистрируем ViewSets
router.register(r'products', ProductViewSet, basename='product')
router.register(r'cart', CartViewSet, basename='cart')
router.register(r'contacts', ContactViewSet, basename='contact')
router.register(r'orders', OrderViewSet, basename='order')

urlpatterns = [
    # Эндпоинты аутентификации
    path('auth/register/', RegisterView.as_view(), name='register'),  # Исправлено: убран префикс api/
    # path('auth/login/', LoginView.as_view(), name='login'),
    path('auth/login/', TokenObtainPairView.as_view(), name='token_obtain_pair'),

    # Эндпоинты для обновления токена
    path('auth/token/refresh/', TokenRefreshView.as_view(), name='token_refresh'),

    # Эндпоинты для заказов
    path('orders/history/', OrderHistoryView.as_view(), name='order-history'),
    
    # Подключаем все зарегистрированные ViewSets
    path('', include(router.urls)),  # Исправлено: убран префикс api/
]