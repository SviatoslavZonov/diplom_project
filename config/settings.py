import os
from pathlib import Path
from datetime import timedelta
import sentry_sdk
from sentry_sdk.integrations.django import DjangoIntegration

# Базовая директория проекта
BASE_DIR = Path(__file__).resolve().parent.parent

# Секретный ключ (заменить надо будет)
SECRET_KEY = 'ваш_секретный_ключ'

# Режим отладки (в продакшене установить DEBUG = False)
# Разрешенные IP-адреса для отображения панели
INTERNAL_IPS = [
    '127.0.0.1',
    '0.0.0.0',  # Для Docker
]
DEBUG = True

# Разрешенные хосты (укажите свои домены или IP)
ALLOWED_HOSTS = ['*']

# Установленные приложения
INSTALLED_APPS = [
    'baton', # панель django-baton
    'cachalot', # django-cachalot
    'debug_toolbar', # визуализация в админке
    'django.contrib.admin',
    'django.contrib.auth',
    'django.contrib.contenttypes',
    'django.contrib.sessions',
    'django.contrib.messages',
    'django.contrib.sites',  # необходимо для allauth
    'django.contrib.staticfiles',
    'rest_framework',
    'drf_spectacular', # добавим генерацию документации DRF-Spectacular
    'corsheaders',
    'imagekit', # django-imagekit для загрузки изображений и создания миниатюр
    'app',  # Мое приложение
    'rest_framework_simplejwt', # добавим библиотеку для возврата токена при авторизации
    'allauth', # добавим авторизацию через соц.сети с помощью django-allauth
    'allauth.account',
    'allauth.socialaccount',
    'allauth.socialaccount.providers.google',
    'baton.autodiscover'
]

SITE_ID = 1  # ID сайта (обычно 1 - дефолт)

# Промежуточное ПО
MIDDLEWARE = [
    'corsheaders.middleware.CorsMiddleware',
    'debug_toolbar.middleware.DebugToolbarMiddleware',
    'django.middleware.security.SecurityMiddleware',
    'django.contrib.sessions.middleware.SessionMiddleware',
    'django.middleware.common.CommonMiddleware',
    'django.middleware.csrf.CsrfViewMiddleware',
    'django.contrib.auth.middleware.AuthenticationMiddleware',
    'django.contrib.messages.middleware.MessageMiddleware',
    'django.middleware.clickjacking.XFrameOptionsMiddleware',
    'allauth.account.middleware.AccountMiddleware', 
]

# Корневой URL-конфиг
ROOT_URLCONF = 'config.urls'

# Шаблоны
TEMPLATES = [
    {
        'BACKEND': 'django.template.backends.django.DjangoTemplates',
        'DIRS': [],
        'APP_DIRS': True,
        'OPTIONS': {
            'context_processors': [
                'django.template.context_processors.debug',
                'django.template.context_processors.request',
                'django.contrib.auth.context_processors.auth',
                'django.contrib.messages.context_processors.messages',
            ],
        },
    },
]

# WSGI-приложение
WSGI_APPLICATION = 'config.wsgi.application'

# # База данных (по умолчанию SQLite для тестирования)
# DATABASES = {
#     'default': {
#         'ENGINE': 'django.db.backends.sqlite3',
#         'NAME': BASE_DIR / 'db.sqlite3',
#     }
# }

# База данных (POSTGRES для production)
DATABASES = {
    'default': {
        'ENGINE': 'django.db.backends.postgresql',
        'NAME': os.getenv('POSTGRES_DB', 'mydb'),
        'USER': os.getenv('POSTGRES_USER', 'admin'),
        'PASSWORD': os.getenv('POSTGRES_PASSWORD', 'password'),
        'HOST': 'db',  # Имя сервиса из docker-compose.yml
        'PORT': 5432,
    }
}

# Валидация паролей
AUTH_PASSWORD_VALIDATORS = [
    {
        'NAME': 'django.contrib.auth.password_validation.UserAttributeSimilarityValidator',
    },
    {
        'NAME': 'django.contrib.auth.password_validation.MinimumLengthValidator',
    },
    {
        'NAME': 'django.contrib.auth.password_validation.CommonPasswordValidator',
    },
    {
        'NAME': 'django.contrib.auth.password_validation.NumericPasswordValidator',
    },
]

# Настройки панели django-baton
BATON = {
    'SITE_HEADER': 'Админ-панель автоматизации закупок',
    'SITE_TITLE': 'Закупки',
    'INDEX_TITLE': 'Управление данными',
    'MENU': [
        {
            'label': 'Пользователи и поставщики',
            'items': [
                {'model': 'app.CustomUser'},
                {'model': 'app.Supplier'},
            ]
        },
        {
            'label': 'Товары и заказы',
            'items': [
                {'model': 'app.Product'},
                {'model': 'app.Order'},
                {'model': 'app.Cart'},
                {'model': 'app.Contact'},
            ]
        },
    ],
    'SUPPORT_HREF': 'https://github.com/your-repo',  # Ссылка на поддержку
}

# Настройки Sentry (логирование ошибок). Получаем DSN из переменных окружения
SENTRY_DSN = os.getenv("SENTRY_DSN")

if SENTRY_DSN:  # Инициализируем только если DSN указан
    sentry_sdk.init(
        dsn=SENTRY_DSN,
        integrations=[DjangoIntegration()],
        traces_sample_rate=1.0,
        send_default_pii=True,
        environment="development" if DEBUG else "production",
        release="v1.0.0",
        before_send=lambda event, hint: None if DEBUG else event,  # Игнорируем ошибки в DEBUG
    )

# Интернационализация
LANGUAGE_CODE = 'ru-ru'
TIME_ZONE = 'Europe/Moscow'
USE_I18N = True
USE_TZ = True

# Статические файлы (CSS, JavaScript, Images)
STATIC_URL = 'static/'
STATIC_ROOT = os.path.join(BASE_DIR, 'static')

# Медиафайлы (загруженные пользователями)
MEDIA_URL = 'media/'
MEDIA_ROOT = os.path.join(BASE_DIR, 'media')

# По умолчанию
DEFAULT_AUTO_FIELD = 'django.db.models.BigAutoField'

# Email settings
EMAIL_BACKEND = 'django.core.mail.backends.smtp.EmailBackend'
EMAIL_HOST = 'smtp.yandex.ru'
EMAIL_PORT = 465  # Для SSL
EMAIL_USE_SSL = True
EMAIL_HOST_USER = 'test1234API@yandex.ru'     # Полный email, нужно разрешить доступ к почтовому ящику с помощью почтовых клиентов в яндексе
EMAIL_HOST_PASSWORD = 'zacrgeogupwyypod'      # Пароль от почты приложения для яндекс айди, SMTP
DEFAULT_FROM_EMAIL = EMAIL_HOST_USER

# REST Framework
REST_FRAMEWORK = {
    'DEFAULT_AUTHENTICATION_CLASSES': [
        'rest_framework_simplejwt.authentication.JWTAuthentication',
    ],
    'DEFAULT_PERMISSION_CLASSES': [
        'rest_framework.permissions.IsAuthenticatedOrReadOnly',
    ],
    'DEFAULT_PAGINATION_CLASS': 'rest_framework.pagination.PageNumberPagination',
    'PAGE_SIZE': 20,

    'DEFAULT_PARSER_CLASSES': [
        'rest_framework.parsers.JSONParser',
        'rest_framework.parsers.FormParser',
    ],
    'DEFAULT_SCHEMA_CLASS': 'drf_spectacular.openapi.AutoSchema', # drf spectacular

    # настройки тротлинга
    'DEFAULT_THROTTLE_CLASSES': [
        'rest_framework.throttling.AnonRateThrottle',
        'rest_framework.throttling.UserRateThrottle'
    ],
    'DEFAULT_THROTTLE_RATES': {
        'anon': '3/minute',  # Лимит для анонимных (вместо 3/minute)
        'user': '5/minute',  # Лимит для авторизованных (вместо 5/minute)
    }
}

# JWT Settings
SIMPLE_JWT = {
    'ACCESS_TOKEN_LIFETIME': timedelta(hours=12),
    'REFRESH_TOKEN_LIFETIME': timedelta(days=7),
    'ROTATE_REFRESH_TOKENS': True,  # Генерировать новый Refresh Token при обновлении
    'BLACKLIST_AFTER_ROTATION': True,
    'SIGNING_KEY': SECRET_KEY,  # Должен совпадать с SECRET_KEY проекта
}

# Настройки Celery
CELERY_BROKER_URL = 'redis://redis:6379/0'  # Локальный Redis
CELERY_RESULT_BACKEND = 'redis://redis:6379/0'
CELERY_TASK_DEFAULT_QUEUE = 'default'

# Настройки Redis 
CACHES = {
    "default": {
        "BACKEND": "django_redis.cache.RedisCache",
        "LOCATION": "redis://redis:6379/1",    
        "OPTIONS": {
            "CLIENT_CLASS": "django_redis.client.DefaultClient",
        },
        "KEY_PREFIX": "myapp_cache"            # префикс ключей
    }
}

# Настройки SPECTACULAR
SPECTACULAR_SETTINGS = {
    'TITLE': 'API для автоматизации закупок',
    'DESCRIPTION': 'Документация API сервиса заказа товаров',
    'VERSION': '1.0.0',
    'SERVE_INCLUDE_SCHEMA': False,
}

# кастомная модель
AUTH_USER_MODEL = 'app.CustomUser'

# Настройки django-allauth для в авторизации через соц.сети
ACCOUNT_LOGIN_METHODS = ["email"]  # Вход только через email
ACCOUNT_SIGNUP_FIELDS = ["email"]  # Обязательные поля при регистрации
ACCOUNT_UNIQUE_EMAIL = True         # Уникальность email

ACCOUNT_AUTHENTICATION_METHOD = 'email'  # Вход по email, а не username
ACCOUNT_EMAIL_REQUIRED = True
ACCOUNT_USERNAME_REQUIRED = False


AUTHENTICATION_BACKENDS = [
    'django.contrib.auth.backends.ModelBackend',
    'allauth.account.auth_backends.AuthenticationBackend',  # Для allauth
]

SOCIALACCOUNT_PROVIDERS = {
    "google": {
        "APP": {
            "client_id": "ВАШ_REAL_CLIENT_ID",
            "secret": "ВАШ_REAL_SECRET",
        },
        "SCOPE": ["profile", "email"],
        "AUTH_PARAMS": {"access_type": "online"},
    }
}

# Настройки django-cachalot
CACHALOT_ENABLED = False  # Отключить кэширование во время миграций
# CACHALOT_ENABLED = True
CACHALOT_TIMEOUT = 60 * 15  # 15 минут

# CORS, если будет фронтенд на отдельном домене
CORS_ALLOW_ALL_ORIGINS = True  # Для разработки, в продакшене указать конкретные домены

# Безопасность (для production)
if not DEBUG:
    SECURE_HSTS_SECONDS = 3600
    SECURE_HSTS_INCLUDE_SUBDOMAINS = True
    SECURE_HSTS_PRELOAD = True
    SECURE_SSL_REDIRECT = True
    SESSION_COOKIE_SECURE = True
    CSRF_COOKIE_SECURE = True

# Для подавления предупреждений (опционально)
STATICFILES_IGNORE_PATTERNS = [
    'admin/css/*',  # Игнорировать конфликтующие файлы
]

# Настройки для работы через Docker debug toolbar
DEBUG_TOOLBAR_CONFIG = {
        'SHOW_TOOLBAR_CALLBACK': lambda request: True,
    }