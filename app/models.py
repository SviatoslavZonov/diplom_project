from django.db import models
from django.conf import settings
from django.core.validators import MinValueValidator
from django.utils.translation import gettext_lazy as _

from django.contrib.auth.models import AbstractUser, BaseUserManager

class CustomUserManager(BaseUserManager):
    def create_user(self, email, password=None, **extra_fields):
        if not email:
            raise ValueError("Email обязателен")
        email = self.normalize_email(email)
        user = self.model(email=email, **extra_fields)
        user.set_password(password)
        user.save(using=self._db)
        return user

    def create_superuser(self, email, password=None, **extra_fields):
        extra_fields.setdefault("is_staff", True)
        extra_fields.setdefault("is_superuser", True)
        return self.create_user(email, password, **extra_fields)

class CustomUser(AbstractUser):
    username = None
    email = models.EmailField("Email", unique=True)
    USERNAME_FIELD = "email"
    REQUIRED_FIELDS = []

    objects = CustomUserManager()  # Используем кастомный менеджер

    def __str__(self):
        return self.email

class Supplier(models.Model):
    name = models.CharField(_("Название"), max_length=100)
    is_active = models.BooleanField(_("Активен"), default=True)
    created_at = models.DateTimeField(_("Дата создания"), auto_now_add=True)
    updated_at = models.DateTimeField(_("Дата обновления"), auto_now=True)

    class Meta:
        verbose_name = _("Поставщик")
        verbose_name_plural = _("Поставщики")

    def __str__(self):
        return self.name

class Product(models.Model):
    name = models.CharField(_("Название"), max_length=100)
    description = models.TextField(_("Описание"), blank=True)
    supplier = models.ForeignKey(
        Supplier,
        on_delete=models.CASCADE,
        verbose_name=_("Поставщик"),
        related_name="products"
    )
    characteristics = models.JSONField(_("Характеристики"), default=dict)
    price = models.DecimalField(
        _("Цена"),
        max_digits=10,
        decimal_places=2,
        validators=[MinValueValidator(0.01)]
    )
    quantity = models.PositiveIntegerField(_("Количество"), default=0)
    created_at = models.DateTimeField(_("Дата создания"), auto_now_add=True)
    updated_at = models.DateTimeField(_("Дата обновления"), auto_now=True)

    class Meta:
        verbose_name = _("Товар")
        verbose_name_plural = _("Товары")
        ordering = ["-created_at"]

    def __str__(self):
        return f"{self.name} ({self.supplier})"

class Cart(models.Model):
    user = models.ForeignKey(
        settings.AUTH_USER_MODEL,
        on_delete=models.CASCADE,
        verbose_name=_("Пользователь"),
        related_name="carts"
    )
    product = models.ForeignKey(
        Product,
        on_delete=models.CASCADE,
        verbose_name=_("Товар")
    )
    quantity = models.PositiveIntegerField(
        _("Количество"),
        default=1,
        validators=[MinValueValidator(1)]
    )
    created_at = models.DateTimeField(_("Дата добавления"), auto_now_add=True)

    class Meta:
        verbose_name = _("Корзина")
        verbose_name_plural = _("Корзины")
        unique_together = [["user", "product"]] # Товар не дублируется в корзине

    def __str__(self):
        return f"{self.user}: {self.product} x{self.quantity}"

class Contact(models.Model):
    user = models.ForeignKey(
        settings.AUTH_USER_MODEL,
        on_delete=models.CASCADE,
        verbose_name=_("Пользователь"),
        related_name="contacts"
    )
    first_name = models.CharField(_("Имя"), max_length=100)
    last_name = models.CharField(_("Фамилия"), max_length=100)
    middle_name = models.CharField(_("Отчество"), max_length=100, blank=True)
    email = models.EmailField(_("Email"))
    phone = models.CharField(_("Телефон"), max_length=20)
    city = models.CharField(_("Город"), max_length=100)
    street = models.CharField(_("Улица"), max_length=100)
    house = models.CharField(_("Дом"), max_length=10)
    building = models.CharField(_("Корпус"), max_length=10, blank=True)
    apartment = models.CharField(_("Квартира"), max_length=10, blank=True)
    created_at = models.DateTimeField(_("Дата создания"), auto_now_add=True)

    class Meta:
        verbose_name = _("Контакт")
        verbose_name_plural = _("Контакты")

    def __str__(self):
        return f"{self.last_name} {self.first_name}"

class Order(models.Model):
    class Status(models.TextChoices):
        PENDING = "pending", _("В обработке")
        PROCESSING = "processing", _("В процессе")
        COMPLETED = "completed", _("Завершен")
        CANCELLED = "cancelled", _("Отменен")

    user = models.ForeignKey(
        settings.AUTH_USER_MODEL,
        on_delete=models.CASCADE,
        verbose_name=_("Пользователь"),
        related_name="orders"
    )
    contact = models.ForeignKey(
        Contact,
        on_delete=models.PROTECT,
        verbose_name=_("Контактные данные")
    )
    status = models.CharField(
        _("Статус"),
        max_length=20,
        choices=Status.choices,
        default=Status.PENDING
    )
    total_price = models.DecimalField(
        _("Общая стоимость"),
        max_digits=12,
        decimal_places=2,
        default=0
    )
    created_at = models.DateTimeField(_("Дата создания"), auto_now_add=True)
    updated_at = models.DateTimeField(_("Дата обновления"), auto_now=True)

    class Meta:
        verbose_name = _("Заказ")
        verbose_name_plural = _("Заказы")
        ordering = ["-created_at"]

    def __str__(self):
        return f"Заказ #{self.id} - {self.get_status_display()}"

class OrderItem(models.Model):
    order = models.ForeignKey(
        Order,
        on_delete=models.CASCADE,
        verbose_name=_("Заказ"),
        related_name="items"
    )
    product = models.ForeignKey(
        Product,
        on_delete=models.PROTECT,
        verbose_name=_("Товар")
    )
    quantity = models.PositiveIntegerField(
        _("Количество"),
        validators=[MinValueValidator(1)]
    )
    price = models.DecimalField(
        _("Цена за единицу"),
        max_digits=10,
        decimal_places=2
    )

    class Meta:
        verbose_name = _("Позиция заказа")
        verbose_name_plural = _("Позиции заказа")

    def __str__(self):
        return f"{self.product} x{self.quantity}"
