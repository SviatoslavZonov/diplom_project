
# Дипломный проект профессии «Python-разработчик: расширенный курс»

## Backend-приложение для автоматизации закупок. Описание проекта
Backend-приложение для автоматизации закупок в розничной сети на **Django Rest Framework**. Сервис предоставляет **REST API** для управления товарами, заказами, пользователями и интеграции с email-уведомлениями.

## Цель проекта
- Автоматизация процессов заказа товаров.
- Управление заказами и поставщиками.
- Интеграция с асинхронными задачами **Celery**.
- Поддержка Docker-контейнеризации.

## Инструкция к работе над проектом

## Основные функции
### Для клиентов:
- Регистрация/авторизация через **JWT**.
- Просмотр каталога товаров.
- Формирование заказов с товарами от разных поставщиков.
- Получение email-уведомлений.

### Для поставщиков:
- Обновление прайс-листов через API.
- Управление статусами заказов.

### Для администраторов:
- Управление пользователями и товарами.
- Запуск импорта данных.
- Мониторинг через Sentry и Django Baton.

### Технологии
- **Python 3.12**, **Django 5.1**, **DRF**
- **PostgreSQL** (основная БД), **Redis** (кеширование)
- **Celery** (асинхронные задачи)
- **Docker** (контейнеризация)
- **Sentry** (мониторинг ошибок)
- **Swagger** (документация API)

## Установка и запуск
### Предварительные установки
Установить:
1. [Docker](https://www.docker.com/) и [Docker Compose](https://docs.docker.com/compose/install/)
2. Python 3.10 или новее
3. Установить IDE с поддержкой Python (например, PyCharm, VS Code).

### Порядок запуска

1. Клонируйте репозиторий:
```bash
   git clone https://github.com/SviatoslavZonov/diplom_project.git
   cd diploma_shop
```

2. Заполните .env (пример).

```.env
POSTGRES_USER=admin
POSTGRES_PASSWORD=secret
POSTGRES_DB=mydb
DEBUG=1
SENTRY_DSN=ваш_DSN
```
3. Запустите контейнеры:
```bash
docker-compose up -d --build
```
1. Сервер доступен по адресу: [https://localhost/](http://localhost:8000)
2. Ознакомьтесь с этапами разработки: [Этапы](https://github.com/netology-code/python-final-diplom/DEVELOPMENT_STAGES.md)

### Тестирование
```bash
docker-compose exec web pytest app/tests/ -v
```
Покрытие кода: 77% (модуль **views.py**).

### Документация API
Swagger: [http://localhost:8000/api/docs/](http://localhost:8000/api/docs/)

Примеры запросов: [requests-examples.http](https://github.com/SviatoslavZonov/diplom_project/blob/main/app/requests-examples.http)
Примеры запросов для проверки администрирования: [requests-examples_admin.http](https://github.com/SviatoslavZonov/diplom_project/blob/main/app/requests-examples_admin.http)

### Контакты
- Автор: Sviatoslav Zonov
- Email: sviatoslavzonov@yandex.ru
- GitHub: [SviatoslavZonov](khttps://github.com/SviatoslavZonov)

Ссылка на задание дипломного проекта: [Диплом](https://github.com/netology-code/python-final-diplom)

## Требования
ОС Linux, MacOS, Windows 10 (WSL)
Python 3.10+
Django 4.2+
Поддерживаемые СУБД: SQLite/PostgreSQL/MySQL
