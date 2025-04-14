import os
from pathlib import Path
from datetime import timedelta

# Базовая директория проекта
BASE_DIR = Path(__file__).resolve().parent.parent

# Секретный ключ (заменить надо будет)
SECRET_KEY = 'ваш_секретный_ключ'

# Режим отладки (в продакшене установить DEBUG = False)
DEBUG = True

# Разрешенные хосты (укажите свои домены или IP)
ALLOWED_HOSTS = ['*']

# Установленные приложения
INSTALLED_APPS = [
    'django.contrib.admin',
    'django.contrib.auth',
    'django.contrib.contenttypes',
    'django.contrib.sessions',
    'django.contrib.messages',
    'django.contrib.staticfiles',
    'rest_framework',
    'corsheaders',
    'app',  # Мое приложение
    'rest_framework_simplejwt', # добавим библиотеку для возврата токена при авторизации
]

# Промежуточное ПО
MIDDLEWARE = [
    'corsheaders.middleware.CorsMiddleware',
    'django.middleware.security.SecurityMiddleware',
    'django.contrib.sessions.middleware.SessionMiddleware',
    'django.middleware.common.CommonMiddleware',
    'django.middleware.csrf.CsrfViewMiddleware',
    'django.contrib.auth.middleware.AuthenticationMiddleware',
    'django.contrib.messages.middleware.MessageMiddleware',
    'django.middleware.clickjacking.XFrameOptionsMiddleware',
]

# кастомная модель
AUTH_USER_MODEL = 'app.CustomUser'

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

# База данных (по умолчанию SQLite)
DATABASES = {
    'default': {
        'ENGINE': 'django.db.backends.sqlite3',
        'NAME': BASE_DIR / 'db.sqlite3',
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
EMAIL_HOST_PASSWORD = '***********'      # Пароль от почты приложения для яндекс айди, SMTP
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
}

# JWT Settings
SIMPLE_JWT = {
    'ACCESS_TOKEN_LIFETIME': timedelta(minutes=60),
    'REFRESH_TOKEN_LIFETIME': timedelta(days=1),
}

# Настройки Celery
CELERY_BROKER_URL = 'redis://localhost:6379/0'  # Локальный Redis
CELERY_RESULT_BACKEND = 'redis://localhost:6379/0'
CELERY_TASK_DEFAULT_QUEUE = 'default'

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