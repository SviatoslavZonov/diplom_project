from django.contrib import admin
from django.urls import path, include
from django.conf import settings
from django.conf.urls.static import static
from drf_spectacular.views import SpectacularAPIView, SpectacularSwaggerView
from django.conf.urls import include
from django.views.generic import RedirectView

urlpatterns = [
    # Админка Django
    path('admin/', admin.site.urls),
    path('baton/', include('baton.urls')),
    # API версии 1
    path('api/', include('app.urls')),

    # маршруты для генерации документации:
    path('api/schema/', SpectacularAPIView.as_view(), name='schema'),
    path('api/docs/', SpectacularSwaggerView.as_view(url_name='schema')), 

    # Перенаправление на /api/ при отсутствие обработчика для корневого URL
    path('', RedirectView.as_view(url='/api/')),
]

# Добавляем поддержку медиафайлов в режиме разработки
if settings.DEBUG:
    urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)
    urlpatterns += static(settings.STATIC_URL, document_root=settings.STATIC_ROOT)
    import debug_toolbar
    urlpatterns += [
        path("__debug__/", include(debug_toolbar.urls)),  # путь debug_toolbar
    ] + urlpatterns