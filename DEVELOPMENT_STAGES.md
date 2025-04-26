# Поэтапная настройка и разработка проекта

## Этап 1. Создание и настройка проекта

### 1. **Клонирование репозитория**
```bash
git clone https://github.com/SviatoslavZonov/diplom_project.git
cd diplom_project
```

### 2. Настройка окружения:
Создайте файл .env с переменными:
```.env
POSTGRES_USER=admin
POSTGRES_PASSWORD=secret
POSTGRES_DB=mydb
DEBUG=1
SENTRY_DSN=ваш_DSN
```
### 3. Установка зависимостей:
```bash
pip install django djangorestframework django-filter celery
```
### 4. Создание проекта и приложения
```bash
django-admin startproject myproject
cd myproject
python manage.py startapp app
```
### 5. Настройка виртуального окружения
- Linux/MacOS:
```bash
python -m venv venv
source venv/bin/activate
```
- Windows:
```cmd
py -m venv venv
venv\Scripts\activate
```
### 6. Установка пакетов
```bash
pip install -r requirements.txt
```
### 7. Запуск сервера разработки
```bash
python manage.py runserver
```

**Проверка:** Откройте http://localhost:8000

## Этап 2. Проработка моделей данных

### 1. Миграций
```bash
python manage.py makemigrations
python manage.py migrate
```
### 2. Проверка моделей
Убедиться, что в приложении app определены модели:
- **Supplier** (поставщики)
- **Product** (товары)
- **Cart** (корзина)
- **Order** (заказы)
- **Contact** (контакты)

## Этап 3. Импорт товаров

### 1. Подготовка данных
Создайте **data/products.yaml**:
```yaml
products:
  - name: "Ноутбук ASUS VivoBook"
    supplier: "TechSupplier"
    price: 899.99
    quantity: 15
    characteristics:
      processor: "Intel Core i5"
      ram: "8 GB"
```
### 2. Запуск импорта
```bash
python manage.py import_products
```
### 3. Проверка данных в Django Admin
Откройте http://localhost:8000/admin


Дополнительные команды: 

|  Действие	                   |  Команда  |
| :---                         |  :---  |
|  Создать суперпользователя	 |  python manage.py createsuperuser  |
|  Очистить базу данных	       |  python manage.py flush  |
|  Запустить тесты	          |  python manage.py test app  |

Для получения **справки** по командам:
```bash
python manage.py help
python manage.py import_products --help
```
**При ошибках:** Удалите db.sqlite3 и файлы в папке app/migrations, заново проведите миграцию:
```bash
python manage.py makemigrations
python manage.py migrate
python manage.py import_products
```

## Этап 4. Реализация API (APIViews)
### Пропишем код всем заявленным критериям:
- Авторизация - реализована через **LoginView** (JWT токены)
- Регистрация - реализована через **RegisterView**
- Получение списка товаров - через **ProductViewSet**
- Получение спецификации по товару - через **ProductViewSet**
- Работа с корзиной - полный CRUD через **CartViewSet**
- Добавление/удаление адреса доставки - через **ContactViewSet**
- Подтверждение заказа - через confirm action в **OrderViewSet **
- Отправка email с подтверждением - реализованы 3 метода отправки email
- Получение списка заказов - через **OrderViewSet** и **OrderHistoryView**
- Получение деталей заказа - через **OrderViewSet**
- Редактирование статуса заказа - через **update_status action**

Дополнительные возможности реализации:
- Использование JWT для аутентификации
- Фильтрация и поиск для товаров
- Автоматический расчет общей суммы заказа
- Раздельные методы для разных типов email-уведомлений
- Проверка прав для всех критических операций

## Этап 5. Полностью готовый backend
### 1. Полностью работающие API Endpoints

| Эндпоинт	                |  Метод	         |  Описание                                                          	| Статус |
| :---                      |     :---:         | :---                                | :---  |                                                   
| /api/auth/register/	    |     POST	         |  Регистрация пользователя. Возвращает JWT-токены.	                   |   Работает  |
| /api/auth/login/	       |     POST	         |  Авторизация пользователя. Возвращает JWT-токены.	                   |   Работает  |
| /api/products/	          |     GET	         |  Получение списка товаров с фильтрацией (supplier, price) и поиском.	 |   Работает  |
| /api/cart/	             |     GET	         |  Просмотр корзины текущего пользователя.	                            |   Работает  |
| /api/cart/	             |     POST	         |  Добавление товара в корзину.	                                        |   Работает  |
| /api/cart/{id}/	          |     PUT/DELETE	   |  Изменение/удаление товара в корзине.	                               |   Работает  |
| /api/contacts/	          |     GET/POST	   |  Просмотр/создание контактов (адресов доставки).	                      |   Работает  |
| /api/contacts/{id}/	    |     PUT/DELETE	   |  Изменение/удаление контакта.	                                        |   Работает  |
| /api/orders/	             |     POST	         |  Создание заказа. Очищает корзину и отправляет email с подтверждением. |	  Работает  |
| /api/orders/{id}/confirm/ |	    POST	         |  Подтверждение заказа (меняет статус на processing).	                |   Работает  |
| /api/orders/history/	    |     GET	         |  Получение истории заказов пользователя.	                            |   Работает  |

### 2. Корректная работа сценариев:
 
| Сценарий	                                          |    Статус	    |    Комментарии  |
| :---                                                |     :---:     | :---                                |                    
| Авторизация	                                       |   Работает	 | JWT-токены возвращаются корректно.  |
| Регистрация	                                       |   Работает    | Email с подтверждением регистрации отправляется.  |
| Добавление товаров в корзину от разных поставщиков	|   Работает	 | Товары добавляются, уникальность контролируется (unique_together в модели).  |
| Создание контактов (адресов доставки)	            |   Работает	 | Контакты сохраняются и привязываются к пользователю.  |
| Подтверждение заказа	                              |   Работает	 | Статус заказа меняется на processing, отправляется email.  |
| Получение email после подтверждения заказа	         |   Работает	 | Письма отправляются при создании и изменении статуса заказа.  |
| Получение списка заказов	                           |   Работает	 | Эндпоинт /api/orders/history/ возвращает историю заказов.  |

Провести тестирование через Postman:
Регистрация → Авторизация → Добавление товаров → Создание контакта → Подтверждение заказа → Проверка истории заказов.

Примеры запросов с описанием в файле [requests-examples.http](./app/requests-examples.http).

## Этап 6. Реализация API views админки склада
### API для администраторов

| Эндпоинт                 | Метод   | Описание                          | Права       |
|  :---  |  :---:  |  :---  |  :---:  |
| `/api/admin/users/`      | GET     | Список всех пользователей        | Только админ|
| `/api/admin/suppliers/`  | POST    | Создание поставщика              | Только админ|
| `/api/admin/orders/`     | GET     | Список всех заказов              | Только админ|
| `/api/admin/orders/{id}/update_status/` | PATCH | Изменение статуса заказа | Только админ|

Примеры запросов с описанием в файле [requests-examples_admin.http](./app/requests-examples_admin.http).

## Этап 7. Вынос медленных методов в задачи Celery
### 1. Создано Celery-приложение c методами:
   - **send_email**,
   - **do_import**.
### 2. Создан view для запуска Celery-задачи do_import из админки.

Установите celery и redis: 
```bash
pip install celery redis
```
Запустите Redis локально (если не используется docker)
Запустите Celery worker:
```bash
celery -A config worker --loglevel=info
```
Запустите Django:
```bash
python manage.py runserver
```

**Проверка:**
Отправьте тестовый заказ → проверьте логи Celery (должно быть Task **send_email** succeeded).
Запустите импорт через API → в логах Celery появится Task **do_import** succeeded.

## Этап 8. Docker-контейнеризация
### 1.Сборка образов:
- **Dockerfile** для Django-приложения.
- **docker-compose.yml** для PostgreSQL, Redis, Celery.
### 2. Запуск:
```bash
docker-compose up -d --build
```
### 3. Миграции в контейнере:
```bash
docker-compose exec web python manage.py migrate
```
### 4. Создайте суперпользователя (при необходимости):
```bash
docker-compose exec web python manage.py createsuperuser
```
### 5. Остановите контейнеры:
```bash
docker-compose down
```

# Дополнительные этапы
## A. Покрыть не менее 30% модуля views.py тестами и проверить это пакетом coverage.
1. Установка зависимостей
```bash
pip install pytest pytest-django coverage django-celery-beat
```
2. Написание тестов в файл **app/tests/test_views.py**
3. Запустим тесты и проверим покрытие:
```bash
coverage run --source='app' -m pytest app/tests/test_views.py -v --ds=config.settings
coverage report -m
```
Результаты покрытия:

|  Name	                |  Stmts	         |  Miss        |  Cover  |  Missing  |
|  :---                 |     :---:          |  :---        |  :---   |  :---     |

|  app/views.py         |  146               |  53          |  64%    |  29-31, 56-69, 87, 93-95, 98-100, 108, 111, 120, 123-140, 144-156, 160-162, 165-167, 170-172, 222, 228-230  |
|  TOTAL                |  452               |  106         | 77%     |           | 

Для генерации HTML-отчета добавьте:
```bash
coverage html && open htmlcov/index.html  # macOS
coverage html && start htmlcov/index.html  # Windows
```

## B. Генерация документации Open API с помощью DRF-Spectacular
1. Установка зависимостей
```bash
pip install drf-spectacular
```
2. Настройка проекта в папке config settings.py и urls.py.
3. Проверка работы
Запустите сервер:
```bash
python manage.py runserver
```
Откройте в браузере:
- Swagger UI: http://localhost:8000/api/docs/
- Redoc UI: http://localhost:8000/api/redoc/

## C. Троттлинг (ограничение ввода незарегистрированных пользователей)
Настройка проекта в папке config settings.py и тестирование.

## D. Авторизация через социальные сети (django-allauth)
1. Установка зависимостей
```bash
pip install django-allauth cryptography
```
2. Настройка проекта в папке config settings.py
3. Миграции:
```bash
python manage.py migrate
```

## E. Кастомизация админ.панели с Django Baton
1. Установка зависимостей
```bash
pip install django-baton
```
2. Настройка проекта в папке config settings.py Добавление маршрутов в urls.py.
3. Миграции:
```bash 
python manage.py migrate
```
4. Сбор статических файлов
```bash 
python manage.py collectstatic
```
5. Проверка работы
Запустите сервер:
```bash
python manage.py runserver
```
Откройте админ-панель: http://localhost:8000/admin/
6. Решение конфликтов allauth с кастомной моделью пользователя реализование через файлы app/backends.py и app/admin_forms.py

## F. Cоздание миниатюр различного размера для быстрой загрузки через django-imagekit
1. Установка зависимостей
```bash
pip install django-imagekit pillow
```
2. Настройка проекта согласно репозитория библиотеки.
3. Проверка работы: создать товар и загрузить изображение через админ.панель.
4. Проверка списка продуктов http://localhost:8000/api/products/

## G. Для проверки стабильности работы внедрим Sentry 
1. Установка зависимостей
```bash
pip install sentry-sdk
```
1. Настройка проекта согласно репозитория библиотеки, в settings.py необходимо внести DSN.
2. Проведем тестовый запрос и добавим эндпоинт в urls. 
Ошибка должна отобразиться в профиле Sentry на sentry.io

Для получения DSN:
- Создайте проект в Sentry.io
- Выберите "Django" в настройках проекта
- Скопируйте DSN из примера кода
Для тестирования в продакшн-режиме в settings.py указать:
```python
DEBUG = False
ALLOWED_HOSTS = ['*']
```

## H. Кэширование с помощью Redis и с помощью django-cachalot измерим производительность 
1. Установка зависимостей
```bash
pip install django-redis django-cachalot
```
2. Настройте Redis в Django и проведите интеграцию django-cachalot.
3. Проверка работы
http://localhost:8000/api/cache-test/
Пример ответа json:
```json
{
  "db_response_time": 0.1254,
  "cached_response_time": 0.0021,
  "speedup": "98.3%"
}
```
4. Визуализация в Django Admin **django-debug-toolbar**
4. 1. Установка зависимостей
```bash
pip install django-debug-toolbar
```
4. 2. Провести настройку файлов согласно репозитория.
4. 3. Debug Toolbar:
Откройте любую страницу проекта в браузере - Панель отладки появится справа.