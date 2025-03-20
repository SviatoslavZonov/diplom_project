from rest_framework import serializers
from django.contrib.auth.models import User
from app.models import Product, Cart, Contact, Order, OrderItem

# Регистрация
class RegisterSerializer(serializers.ModelSerializer):
    password = serializers.CharField(write_only=True, min_length=8)
    email = serializers.EmailField()

    class Meta:
        model = User
        fields = ['first_name', 'last_name', 'email', 'password']

    def validate_email(self, value):
        if User.objects.filter(email=value).exists():
            raise serializers.ValidationError("This email is already in use.")
        return value

    def create(self, validated_data):
        user = User.objects.create_user(
            username=validated_data['email'],
            email=validated_data['email'],
            password=validated_data['password'],
            first_name=validated_data['first_name'],
            last_name=validated_data['last_name']
        )
        return user

# Авторизация
class LoginSerializer(serializers.Serializer):
    email = serializers.EmailField()
    password = serializers.CharField()

    def validate(self, data):
        email = data.get('email')
        password = data.get('password')

        if not email or not password:
            raise serializers.ValidationError("Email and password are required.")

        return data

# Товар
class ProductSerializer(serializers.ModelSerializer):
    class Meta:
        model = Product
        fields = ['id', 'name', 'description', 'supplier', 'characteristics', 'price', 'quantity']

    def validate_price(self, value):
        if value <= 0:
            raise serializers.ValidationError("Price must be greater than 0.")
        return value

    def validate_quantity(self, value):
        if value < 0:
            raise serializers.ValidationError("Quantity cannot be negative.")
        return value

# Корзина
class CartSerializer(serializers.ModelSerializer):
    class Meta:
        model = Cart
        fields = ['id', 'user', 'product', 'quantity']

    def validate_quantity(self, value):
        if value < 1:
            raise serializers.ValidationError("Quantity must be at least 1.")
        return value

# Контакт
class ContactSerializer(serializers.ModelSerializer):
    class Meta:
        model = Contact
        fields = '__all__'

    def validate_phone(self, value):
        if not value.isdigit():
            raise serializers.ValidationError("Phone number must contain only digits.")
        return value

    def validate_email(self, value):
        if not value:
            raise serializers.ValidationError("Email is required.")
        return value

# Элемент заказа
class OrderItemSerializer(serializers.ModelSerializer):
    class Meta:
        model = OrderItem
        fields = '__all__'

# Заказ
class OrderSerializer(serializers.ModelSerializer):
    items = OrderItemSerializer(many=True, read_only=True)

    class Meta:
        model = Order
        fields = '__all__'

    def validate_status(self, value):
        valid_statuses = ['pending', 'completed', 'cancelled']
        if value not in valid_statuses:
            raise serializers.ValidationError(f"Invalid status. Must be one of {valid_statuses}.")
        return value