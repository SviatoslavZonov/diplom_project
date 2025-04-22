import os
import sentry_sdk
from rest_framework import viewsets, generics, status, permissions, serializers
from rest_framework.permissions import IsAdminUser
from rest_framework.response import Response
from rest_framework.views import APIView
from rest_framework_simplejwt.views import TokenObtainPairView
from rest_framework_simplejwt.tokens import RefreshToken
from django_filters.rest_framework import DjangoFilterBackend
from rest_framework import filters
from rest_framework.decorators import action
from django.core.mail import send_mail
from django.conf import settings
from django.contrib.auth import get_user_model
from django.shortcuts import render
from .models import CustomUser, Product, Cart, Contact, Order, OrderItem, Supplier
from .serializers import (
    ProductSerializer, CartSerializer,
    ContactSerializer, OrderSerializer,
    LoginSerializer, RegisterSerializer
)
from app.tasks import send_email, do_import

from django.db.models.signals import post_save
from django.dispatch import receiver
from .tasks import generate_image_thumbnails

from django.shortcuts import render

@receiver(post_save, sender=Product)
def process_product_image(sender, instance, **kwargs):
    if instance.image:
        generate_image_thumbnails.delay(instance.id)

User = get_user_model()

# список продуктов
def product_list(request):
    products = Product.objects.all()
    return render(request, 'products/list.html', {'products': products})

## Админмстраторы
# запуск импорта через API асинхронно
class AdminViewSet(viewsets.ViewSet):
    @action(detail=False, methods=['post'], permission_classes=[permissions.IsAdminUser])
    def run_import(self, request):
        path = os.path.join(settings.BASE_DIR, 'data')
        do_import.delay(path)  # Асинхронный запуск
        return Response({"status": "Импорт запущен"}, status=200)

# Управление пользователями (администратор)
class AdminUserViewSet(viewsets.ModelViewSet):
    queryset = CustomUser.objects.all()
    serializer_class = RegisterSerializer  # Используем существующий сериализатор
    permission_classes = [IsAdminUser]
    http_method_names = ['get', 'post', 'patch', 'delete']  # Запрет на PUT

# Управление поставщиками (администратор)
class AdminSupplierViewSet(viewsets.ModelViewSet):
    queryset = Supplier.objects.all()
    serializer_class = serializers.Serializer  # Нужно создать SupplierSerializer
    permission_classes = [IsAdminUser]

# Управление всеми заказами (администратор)
class AdminOrderViewSet(viewsets.ModelViewSet):
    queryset = Order.objects.all()
    serializer_class = OrderSerializer
    permission_classes = [IsAdminUser]
    filter_backends = [filters.SearchFilter]
    search_fields = ['user__email', 'status']

    @action(detail=True, methods=['patch'])
    def update_status(self, request, pk=None):
        order = self.get_object()
        new_status = request.data.get('status')
                
        if not new_status or new_status not in dict(Order.Status.choices):
            return Response({'error': 'Неверный статус'}, 
                          status=status.HTTP_400_BAD_REQUEST)
            
        order.status = new_status
        order.save()
        
        if new_status == Order.Status.COMPLETED:
            self.send_completion_email(order)
            
        return Response(OrderSerializer(order).data)

## Пользователи
# Товары
class ProductViewSet(viewsets.ModelViewSet):
    queryset = Product.objects.all()
    serializer_class = ProductSerializer
    filter_backends = [DjangoFilterBackend, filters.SearchFilter]
    filterset_fields = ['supplier', 'price']
    search_fields = ['name', 'description']
    permission_classes = [permissions.IsAuthenticatedOrReadOnly]

# Корзина
class CartViewSet(viewsets.ModelViewSet):
    serializer_class = CartSerializer
    permission_classes = [permissions.IsAuthenticated]

    def get_queryset(self):
        return Cart.objects.filter(user=self.request.user)

    def perform_create(self, serializer):
        serializer.save(user=self.request.user)

    def perform_update(self, serializer):
        if serializer.instance.user != self.request.user:
            raise permissions.PermissionDenied("Нет прав для изменения этой корзины")
        serializer.save()

    def perform_destroy(self, instance):
        if instance.user != self.request.user:
            raise permissions.PermissionDenied("Нет прав для удаления этой корзины")
        instance.delete()

# Контакты
class ContactViewSet(viewsets.ModelViewSet):
    serializer_class = ContactSerializer
    permission_classes = [permissions.IsAuthenticated]

    def get_queryset(self):
        return Contact.objects.filter(user=self.request.user)

    def perform_create(self, serializer):
        serializer.save(user=self.request.user)

# Заказы
class OrderViewSet(viewsets.ModelViewSet):
    serializer_class = OrderSerializer
    permission_classes = [permissions.IsAuthenticated]
    queryset = Order.objects.all()

    def get_queryset(self):
        return Order.objects.filter(user=self.request.user)

    def perform_create(self, serializer):
        cart_items = Cart.objects.filter(user=self.request.user)
        if not cart_items.exists():
            raise serializers.ValidationError("Корзина пуста")

        total_price = sum(item.product.price * item.quantity for item in cart_items)
        order = serializer.save(user=self.request.user, total_price=total_price)
        
        # Создаем OrderItems
        for item in cart_items:
            OrderItem.objects.create(
                order=order,
                product=item.product,
                quantity=item.quantity,
                price=item.product.price
            )
        
        cart_items.delete()
        self.send_order_email(order)

    @action(detail=True, methods=['post'])
    def confirm(self, request, pk=None):
        order = self.get_object()
        if order.user != request.user:
            return Response({'error': 'Недостаточно прав'}, status=status.HTTP_403_FORBIDDEN)
        
        if order.status != Order.Status.PENDING:
            return Response({'error': 'Заказ уже обрабатывается или завершен'}, 
                          status=status.HTTP_400_BAD_REQUEST)
        
        order.status = Order.Status.PROCESSING
        order.save()
        self.send_confirmation_email(order)
        
        return Response({'status': 'Заказ подтвержден'}, status=status.HTTP_200_OK)

# Заменим вызовы send_mail на асинхронные задачи
    def send_order_email(self, order):
        subject = f'Новый заказ #{order.id}'
        message = f'Ваш заказ #{order.id} успешно создан. Статус: {order.get_status_display()}'
        send_email.delay(subject, message, [order.user.email])  # Вызов задачи

    def send_confirmation_email(self, order):
        subject = f'Заказ #{order.id} подтвержден'
        message = f'Ваш заказ #{order.id} передан в обработку.'
        send_email.delay(subject, message, [order.user.email])

    def send_completion_email(self, order):
        subject = f'Заказ #{order.id} завершен'
        message = f'Ваш заказ #{order.id} успешно завершен.'
        send_email.delay(subject, message, [order.user.email])

# Регистрация
class RegisterView(APIView):
    permission_classes = [permissions.AllowAny]

    def post(self, request):
        serializer = RegisterSerializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        user = serializer.save()

        # Отправляем email с подтверждением регистрации
        self.send_registration_email(user)

        refresh = RefreshToken.for_user(user)
        return Response({
            "user": RegisterSerializer(user).data,
            "refresh": str(refresh),
            "access": str(refresh.access_token)
        }, status=status.HTTP_201_CREATED)

    def send_registration_email(self, user):
        subject = 'Подтверждение регистрации'
        message = (
            f'Здравствуйте, {user.first_name} {user.last_name}!\n\n'
            'Благодарим за регистрацию в сервисе автоматизации закупок.\n'
            'Ваш аккаунт успешно создан.\n\n'
            'С уважением, команда сервиса.'
        )
        send_mail(
            subject,
            message,
            settings.DEFAULT_FROM_EMAIL,
            [user.email],
            fail_silently=False,
        )

# Авторизация
class LoginView(TokenObtainPairView):
    serializer_class = LoginSerializer
    permission_classes = [permissions.AllowAny]

# История заказов
class OrderHistoryView(generics.ListAPIView):
    serializer_class = OrderSerializer
    permission_classes = [permissions.IsAuthenticated]
    filter_backends = [filters.OrderingFilter]
    ordering_fields = ['created_at']

    def get_queryset(self):
        return Order.objects.filter(user=self.request.user)

# запуск импорта через API асинхронно
class AdminViewSet(viewsets.ViewSet):
    @action(detail=False, methods=['post'], permission_classes=[permissions.IsAdminUser])
    def run_import(self, request):
        path = os.path.join(settings.BASE_DIR, 'data')
        do_import.delay(path)  # Асинхронный запуск
        return Response({"status": "Импорт запущен"}, status=200)

# Sentry, тестовый эндпоинт для генерации ошибки
class SentryTestView(APIView):
    def get(self, request):
        try:
            # Генерируем цепочку исключений
            result = 1 / 0
        except ZeroDivisionError as e:
            # Добавляем кастомный контекст
            with sentry_sdk.configure_scope() as scope:
                scope.set_tag("test_tag", "sentry_debug")
                scope.set_extra("debug_info", {
                    "user": str(request.user),
                    "path": request.path
                })
            
            # Логируем через Sentry
            sentry_sdk.capture_exception(e)
            
            # Возвращаем кастомный ответ
            return Response(
                {"error": "Тестовая ошибка залогирована в Sentry"},
                status=status.HTTP_500_INTERNAL_SERVER_ERROR
            )