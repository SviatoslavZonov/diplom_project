from django.contrib import admin
from django.urls import path, include
from django.conf import settings
from django.conf.urls.static import static

urlpatterns = [
    # Админка Django
    path('admin/', admin.site.urls),
    # API версии 1
    path('api/', include('app.urls')),  # Префикс v1/ уберем
    # path('api/v1/', include('app.urls')),  # Префикс api/v1/ остается
]

# Добавляем поддержку медиафайлов в режиме разработки
if settings.DEBUG:
    urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)
    urlpatterns += static(settings.STATIC_URL, document_root=settings.STATIC_ROOT)