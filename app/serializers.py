from rest_framework import serializers
from django.contrib.auth import get_user_model
from app.models import Product, Cart, Contact, Order, OrderItem, Supplier

from django.core.validators import MinValueValidator

User = get_user_model()

# Сериализатор для поставщиков (админ)
class SupplierSerializer(serializers.ModelSerializer):
    class Meta:
        model = Supplier
        fields = '__all__'

# Регистрация
class RegisterSerializer(serializers.ModelSerializer):
    password = serializers.CharField(
        write_only=True,
        min_length=8,
        style={'input_type': 'password'}
    )
    email = serializers.EmailField(required=True)

    class Meta:
        model = User
        fields = ['first_name', 'last_name', 'email', 'password']

    def validate_email(self, value):
        if User.objects.filter(email=value).exists():
            raise serializers.ValidationError("Email уже используется")
        return value

    def create(self, validated_data):
        return User.objects.create_user(
            email=validated_data['email'],
            password=validated_data['password'],
            first_name=validated_data['first_name'],
            last_name=validated_data['last_name']
        )

# Авторизация
class LoginSerializer(serializers.Serializer):
    email = serializers.EmailField(required=True)
    password = serializers.CharField(
        style={'input_type': 'password'},
        trim_whitespace=False
    )

    def validate(self, attrs):
        attrs = super().validate(attrs)
        if not attrs.get('email') or not attrs.get('password'):
            raise serializers.ValidationError("Необходимо указать email и пароль")
        return attrs

# Товар
class ProductSerializer(serializers.ModelSerializer):
    supplier = serializers.StringRelatedField()

    class Meta:
        model = Product
        fields = [
            'id', 
            'name', 
            'description', 
            'supplier', 
            'characteristics', 
            'price', 
            'quantity',
            'created_at'
        ]
        read_only_fields = ['created_at']

    def validate_price(self, value):
        if value <= 0:
            raise serializers.ValidationError("Цена должна быть больше 0")
        return value

    def validate_quantity(self, value):
        if value < 0:
            raise serializers.ValidationError("Количество не может быть отрицательным")
        return value

# Корзина
class CartSerializer(serializers.ModelSerializer):
    product = ProductSerializer(read_only=True)
    product_id = serializers.PrimaryKeyRelatedField(
        queryset=Product.objects.all(),
        source="product",
        write_only=True
    )
    quantity = serializers.IntegerField(  # Явно указываем тип
        default=1,
        validators=[MinValueValidator(1)]  # меняем валидатор
    )

    class Meta:
        model = Cart
        fields = [
            "id",
            "product",
            "product_id",
            "quantity",
            "created_at"
        ]
        read_only_fields = ["created_at"]

    def validate_quantity(self, value):
        if value < 1:
            raise serializers.ValidationError("Количество должно быть не менее 1")
        return value

# Контакт
class ContactSerializer(serializers.ModelSerializer):
    class Meta:
        model = Contact
        fields = [
            'id',
            'first_name',
            'last_name',
            'middle_name',
            'email',
            'phone',
            'city',
            'street',
            'house',
            'building',
            'apartment',
            'created_at'
        ]
        read_only_fields = ['created_at']

    def validate_phone(self, value):
        if not value.isdigit():
            raise serializers.ValidationError("Телефон должен содержать только цифры")
        return value

# Элемент заказа
class OrderItemSerializer(serializers.ModelSerializer):
    product = ProductSerializer(read_only=True)

    class Meta:
        model = OrderItem
        fields = [
            'id',
            'product',
            'quantity',
            'price'
        ]

# Заказ
class OrderSerializer(serializers.ModelSerializer):
    items = OrderItemSerializer(many=True, read_only=True)
    status = serializers.ChoiceField(
        choices=Order.Status.choices,
        default=Order.Status.PENDING
    )

    class Meta:
        model = Order
        fields = [
            'id',
            'status',
            'total_price',
            'items',
            'contact',
            'created_at',
            'updated_at'
        ]
        read_only_fields = [
            'total_price',
            'created_at',
            'updated_at'
        ]

    def validate_status(self, value):
        valid_statuses = dict(Order.Status.choices).keys()
        if value not in valid_statuses:
            raise serializers.ValidationError(
                f"Недопустимый статус. Допустимые значения: {', '.join(valid_statuses)}"
            )
        return value
