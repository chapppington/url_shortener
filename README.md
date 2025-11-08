# URL Shortener

REST API для сокращения URL, построенное на принципах Domain-Driven Design.

## Описание

Приложение предоставляет API для:
- Создания коротких ссылок из длинных URL
- Получения длинных URL по коротким ссылкам

## Стек технологий

### Backend
- **Python 3.13** - язык программирования
- **FastAPI** - веб-фреймворк для REST API
- **Uvicorn** - ASGI сервер
- **Pydantic** - валидация данных и настройки
- **SQLAlchemy 2.0** - ORM для работы с БД
- **Alembic** - миграции базы данных
- **asyncpg** - асинхронный драйвер PostgreSQL
- **punq** - DI контейнер
- **Redis** - кэширование
- **base62** - кодирование URL

### Инфраструктура
- **PostgreSQL** - основная база данных
- **Redis** - кэш
- **pgAdmin** - администрирование PostgreSQL
- **RedisInsight** - администрирование Redis
- **Docker** - контейнеризация

### Инструменты разработки
- **pytest** - тестирование
- **pytest-asyncio** - асинхронные тесты
- **isort** - сортировка импортов
- **pre-commit** - хуки для проверки кода
- **faker** - генерация тестовых данных

### Архитектурные паттерны
- **DDD (Domain-Driven Design)** - проектирование на основе предметной области
- **CQRS** - разделение команд и запросов через Mediator
- **Repository Pattern** - абстракция работы с данными
- **Dependency Injection** - через punq контейнер
- **Value Objects** - валидация доменных объектов (URL)

## Запуск проекта

1. Настройте переменные окружения в `.env`:
```env
API_PORT=8000
PYTHONPATH=/app

POSTGRES_DB=url_shortener
POSTGRES_USER=postgres
POSTGRES_PASSWORD=postgres
POSTGRES_HOST=postgres
POSTGRES_PORT=5432

PGADMIN_DEFAULT_EMAIL=admin@admin.com
PGADMIN_DEFAULT_PASSWORD=admin
PGADMIN_PORT=5050

REDIS_HOST=redis
REDIS_PORT=6379
REDISINSIGHT_PORT=5540
```

2. Запустите приложение:
```bash
make all
```

3. Примените миграции:
```bash
make migrate
```

## API

После запуска API документация доступна по адресу:
- Swagger UI: `http://localhost:8000/api/docs`

### Формат ответов

Все ответы API возвращаются в едином формате `ApiResponse`:

**Успешный ответ:**
```json
{
  "data": {
    "short_url": "abc123"
  },
  "meta": {},
  "errors": []
}
```

**Ответ с ошибкой:**
```json
{
  "data": {},
  "meta": {},
  "errors": ["URL must include a scheme (e.g., http:// or https://)"]
}
```

### Валидация URL

При создании короткой ссылки URL валидируется по следующим правилам:
- URL не может быть пустым
- URL должен содержать схему (`http://` или `https://`)
- URL должен содержать домен (например, `example.com`)
- Поддерживаются только схемы `http` и `https`
- Максимальная длина URL: 2048 символов

### Эндпоинты

- `POST /api/v1/urls` - создание короткой ссылки
  ```json
  {
    "long_url": "https://example.com"
  }
  ```
  **Примеры ошибок:**
  - Пустой URL: `{"errors": ["URL cannot be empty"]}`
  - URL без схемы: `{"errors": ["Invalid URL 'example.com': URL must include a scheme (e.g., http:// or https://)"]}`
  - Неподдерживаемая схема: `{"errors": ["Invalid URL 'ftp://example.com': Unsupported scheme 'ftp'. Only http and https are allowed"]}`

- `GET /api/v1/urls/{short_url}` - получение длинной ссылки по короткой
  **Пример ошибки:**
  - URL не найден: `{"errors": ["Long URL not found for short URL: abc123"]}`

## Тестирование

```bash
# Запуск тестов
make test
```

## Архитектура

Проект разделен на слои DDD:

- **Domain** - бизнес-логика и сущности
- **Application** - команды и запросы (CQRS)
- **Infrastructure** - репозитории, модели БД
- **Presentation** - API endpoints

## Команды Makefile

- `make all` - запуск всех сервисов
- `make all-down` - остановка всех сервисов
- `make test` - запуск тестов
- `make migrate` - применение миграций
- `make migrations` - создание новой миграции
