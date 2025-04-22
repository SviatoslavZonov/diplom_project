from django.contrib import admin
from django.contrib.auth.admin import UserAdmin
from django.contrib.admin.forms import AdminAuthenticationForm
from django import forms
from .models import CustomUser, Product

# Кастомная форма аутентификации для админки
class CustomAdminAuthForm(AdminAuthenticationForm):
    username = forms.EmailField(
        label="Email",
        widget=forms.EmailInput(attrs={'autofocus': True})
    )

# Применяем кастомную форму для входа
admin.site.login_form = CustomAdminAuthForm

@admin.register(CustomUser)
class CustomUserAdmin(UserAdmin):
    fieldsets = (
        (None, {"fields": ("email", "password")}),
        ("Персональная информация", {"fields": ("first_name", "last_name")}),
        ("Права доступа", {"fields": ("is_active", "is_staff", "is_superuser", "groups", "user_permissions")}),
    )
    list_display = ("email", "first_name", "last_name", "is_staff")
    ordering = ("email",)

# Модель Product для загрузки изображений
@admin.register(Product)
class ProductAdmin(admin.ModelAdmin):
    list_display = ('name', 'supplier', 'price')
    readonly_fields = ('thumbnail_preview',)  # Покажет превью миниатюры

    def thumbnail_preview(self, obj):
        if obj.thumbnail:
            return obj.thumbnail.url
        return "Нет изображения"
    
    thumbnail_preview.short_description = "Миниатюра"