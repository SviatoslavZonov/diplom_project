from django.contrib import admin
from django.urls import path, include
from django.conf import settings
from django.conf.urls.static import static

urlpatterns = [
    # Админка Django
    path('admin/', admin.site.urls),
    
    # API версии 1
    path('api/v1/', include(('app.urls', 'app'), namespace='v1')),
    
    # Дополнительные маршруты (если есть)
    # path('api/v2/', include(('app.v2.urls', 'app'), namespace='v2')),
]

# Добавляем поддержку медиафайлов в режиме разработки
if settings.DEBUG:
    urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)
    urlpatterns += static(settings.STATIC_URL, document_root=settings.STATIC_ROOT)