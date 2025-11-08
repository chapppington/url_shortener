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
- **Elastic APM** - мониторинг производительности и отслеживание ошибок

### Инфраструктура
- **PostgreSQL** - основная база данных
- **Redis** - кэш
- **pgAdmin** - администрирование PostgreSQL
- **RedisInsight** - администрирование Redis
- **Elasticsearch** - хранилище для APM данных
- **Kibana** - визуализация метрик и ошибок APM
- **APM Server** - сбор и обработка данных мониторинга
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

# Elastic APM configuration
ELASTIC_APM_SERVER_URL=http://apm-server:8200
ELASTIC_APM_SERVICE_NAME=url-shortener
ELASTIC_APM_DEBUG=false
ELASTIC_APM_ENVIRONMENT=prod
ELASTIC_APM_CAPTURE_BODY=all
ELASTIC_APM_CAPTURE_HEADERS=true
ELASTIC_APM_USE_ELASTIC_EXCEPTHOOK=true
```

2. Запустите приложение:
```bash
# Запуск только приложения и хранилищ
make all

# Запуск приложения с мониторингом (Elasticsearch, Kibana, APM Server)
make all-with-monitoring
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

## Мониторинг и APM

Приложение интегрировано с **Elastic APM** для мониторинга производительности и отслеживания ошибок.

<img width="1728" height="914" alt="Снимок экрана 2025-11-08 в 09 53 16" src="https://github.com/user-attachments/assets/835f9d8a-f62a-47e5-9c0b-661beb78dafd" />

<img width="1725" height="992" alt="Снимок экрана 2025-11-08 в 09 53 07" src="https://github.com/user-attachments/assets/8fc36a35-1edd-4d0a-b511-a1c1cc019cbe" />


### Возможности мониторинга

- **Трассировка запросов** - отслеживание времени выполнения запросов и их компонентов (app, PostgreSQL, Redis)
- **Отслеживание ошибок** - автоматическая отправка всех исключений (DomainException, HTTPException 4xx/5xx, необработанные исключения) в APM
- **Метрики производительности** - мониторинг транзакций, задержек, throughput
- **Визуализация в Kibana** - дашборды для анализа производительности и ошибок

### Доступ к мониторингу

После запуска с мониторингом (`make all-with-monitoring`):

- **Kibana APM**: `http://localhost:5601` → перейдите в раздел APM
- **Elasticsearch**: `http://localhost:9200`
- **APM Server**: `http://localhost:8200`

### Просмотр ошибок

Все ошибки автоматически отправляются в APM и отображаются во вкладке **Errors** в Kibana:
- HTTP 4xx ошибки (валидация, неверные запросы)
- HTTP 5xx ошибки (серверные ошибки)
- Доменные исключения (DomainException)
- Необработанные исключения

Ошибки также видны в разделе **Transactions** с фильтром по статус-кодам.

## Команды Makefile

### Основные команды
- `make all` - запуск приложения и хранилищ
- `make all-down` - остановка приложения и хранилищ
- `make all-with-monitoring` - запуск приложения с мониторингом
- `make all-with-monitoring-down` - остановка приложения и мониторинга

### Тестирование и миграции
- `make test` - запуск тестов
- `make migrate` - применение миграций
- `make migrations` - создание новой миграции

### Мониторинг
- `make monitoring` - запуск только мониторинга
- `make monitoring-down` - остановка мониторинга
- `make monitoring-logs` - логи мониторинга
- `make elasticsearch-logs` - логи Elasticsearch
- `make apm-logs` - логи APM Server
- `make kibana-logs` - логи Kibana
