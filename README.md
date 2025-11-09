# URL Shortener

REST API для сокращения URL, построенное на принципах Domain-Driven Design.

<img width="1464" height="445" alt="Снимок экрана 2025-11-08 в 10 03 00" src="https://github.com/user-attachments/assets/e477d742-762f-419f-9186-71bf29dfe4b0" />


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

## Мониторинг

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

- **Kibana**: `http://localhost:5601` → перейдите в раздел APM
- **Elasticsearch**: `http://localhost:9200`
- **APM Server**: `http://localhost:8200`

### Просмотр ошибок

Все ошибки автоматически отправляются в APM и отображаются во вкладке **Errors** в Kibana:
- HTTP 4xx ошибки (валидация, неверные запросы)
- HTTP 5xx ошибки (серверные ошибки)
- Доменные исключения (DomainException)
- Необработанные исключения

Ошибки также видны в разделе **Transactions** с фильтром по статус-кодам.

## Деплой на VPS

Проект настроен для автоматического деплоя на VPS через GitHub Actions.

### Настройка GitHub Secrets

Для работы автоматического деплоя необходимо настроить следующие секреты в GitHub:

**Необходимые секреты:**
- `VPS_SSH_PRIVATE_KEY` - приватный SSH ключ для доступа к VPS
- `VPS_HOST` - IP адрес или домен VPS сервера
- `VPS_USER` - имя пользователя для SSH подключения (обычно `root` или `ubuntu`)
- `VPS_APP_DIR` - путь к директории проекта на сервере (например, `/opt/url_shortener`)
- `VPS_APP_URL` - (опционально) URL приложения для health check (например, `http://your-domain.com`)

**Подробные инструкции по настройке SSH ключа и добавлению секретов см. ниже в разделе "Подготовка VPS сервера" (шаги 2 и 5).**

### Подготовка VPS сервера

1. **Установите необходимые зависимости:**
   ```bash
   # Обновление системы
   sudo apt update && sudo apt upgrade -y
   
   # Установка Docker и Docker Compose
   curl -fsSL https://get.docker.com -o get-docker.sh
   sudo sh get-docker.sh
   sudo apt install docker-compose-plugin -y
   
   # Установка Git
   sudo apt install git -y
   ```

2. **Настройте SSH ключ для GitHub Actions:**
   
   **Шаг 1: Создайте SSH ключ (на вашей локальной машине)**
   ```bash
   # Сгенерируйте новый SSH ключ специально для GitHub Actions
   ssh-keygen -t ed25519 -C "github-actions-deploy" -f ~/.ssh/github_actions_deploy
   
   # Или используйте существующий ключ (если у вас уже есть SSH ключ для VPS)
   # В этом случае пропустите этот шаг
   ```
   
   **Шаг 2: Скопируйте публичный ключ на VPS сервер**
   ```bash
   # Если создали новый ключ
   ssh-copy-id -i ~/.ssh/github_actions_deploy.pub user@your-vps-ip
   
   # Или если используете существующий ключ
   ssh-copy-id user@your-vps-ip
   
   # Проверьте подключение
   ssh -i ~/.ssh/github_actions_deploy user@your-vps-ip
   # или
   ssh user@your-vps-ip
   ```
   
   **Шаг 3: Скопируйте приватный ключ для GitHub Secrets**
   ```bash
   # Если создали новый ключ
   cat ~/.ssh/github_actions_deploy
   
   # Или если используете существующий ключ (обычно ~/.ssh/id_ed25519 или ~/.ssh/id_rsa)
   cat ~/.ssh/id_ed25519
   # или
   cat ~/.ssh/id_rsa
   ```
   
   **Важно:** Скопируйте весь вывод команды (включая строки `-----BEGIN OPENSSH PRIVATE KEY-----` и `-----END OPENSSH PRIVATE KEY-----`)

3. **Клонируйте репозиторий на сервер:**
   ```bash
   cd /opt
   sudo git clone https://github.com/your-username/url_shortener.git
   sudo chown -R $USER:$USER url_shortener
   cd url_shortener
   ```

4. **Создайте файл `.env` на сервере:**
   ```bash
   # Скопируйте пример .env и отредактируйте под продакшн
   cp .env.example .env
   nano .env
   ```
   
   Обновите переменные для продакшн окружения:
   ```env
   API_PORT=8000
   POSTGRES_HOST=postgres
   POSTGRES_PORT=5432
   # ... остальные переменные
   ```

5. **Добавьте SSH ключ в GitHub Secrets:**
   
   **Шаг 1: Откройте настройки репозитория в GitHub**
   - Перейдите в ваш репозиторий на GitHub
   - Нажмите на **Settings** (в верхней панели)
   - В левом меню выберите **Secrets and variables** → **Actions**
   
   **Шаг 2: Добавьте секреты**
   
   Нажмите **New repository secret** и добавьте каждый секрет:
   
   - **Name:** `VPS_SSH_PRIVATE_KEY`
     **Value:** Вставьте весь приватный ключ (который вы скопировали на шаге 2.3)
     - Должен начинаться с `-----BEGIN OPENSSH PRIVATE KEY-----`
     - И заканчиваться на `-----END OPENSSH PRIVATE KEY-----`
     - Включая все строки между ними
   
   - **Name:** `VPS_HOST`
     **Value:** IP адрес или домен вашего VPS (например, `123.45.67.89` или `example.com`)
   
   - **Name:** `VPS_USER`
     **Value:** Имя пользователя для SSH (обычно `root`, `ubuntu`, или `debian`)
   
   - **Name:** `VPS_APP_DIR`
     **Value:** Путь к директории проекта на сервере (например, `/opt/url_shortener`)
   
   - **Name:** `VPS_APP_URL` (опционально)
     **Value:** URL вашего приложения для health check (например, `http://your-domain.com` или `https://api.example.com`)
   
   **Важно:** После добавления секретов они будут зашифрованы и их нельзя будет просмотреть. Убедитесь, что сохранили значения где-то безопасно.

### Автоматический деплой

После настройки, деплой будет автоматически запускаться при:
- Push в ветку `master` или `main`
- Ручном запуске через GitHub Actions (Actions → Deploy to VPS → Run workflow)

**Важно:** Перед деплоем автоматически выполняются проверки:
1. **Линтинг кода** - проверка стиля кода с помощью `ruff` и `isort`
2. **Тесты** - запуск всех тестов через `pytest`

Деплой на VPS произойдет **только если** все проверки пройдут успешно. Это гарантирует, что на продакшн попадает только проверенный код.

### Ручной деплой

Для ручного деплоя можно использовать скрипт `deploy.sh`:

```bash
# На сервере
cd /opt/url_shortener
./deploy.sh master
```

### Что делает деплой

1. Обновляет код из репозитория
2. Останавливает старые контейнеры
3. Собирает новые Docker образы
4. Запускает контейнеры
5. Применяет миграции базы данных
6. Очищает неиспользуемые Docker образы
7. Проверяет статус контейнеров

### Откат к предыдущей версии

Если нужно откатиться к предыдущей версии:

```bash
cd /opt/url_shortener
git log --oneline  # найти нужный коммит
git reset --hard <commit-hash>
./deploy.sh
```

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
