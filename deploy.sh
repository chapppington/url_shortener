#!/bin/bash

# Скрипт для деплоя на VPS
# Использование: ./deploy.sh [branch]
# По умолчанию деплоится ветка master

set -e

BRANCH=${1:-master}
APP_DIR=${VPS_APP_DIR:-$(pwd)}

echo "🚀 Starting deployment of branch: $BRANCH"

# Переходим в директорию проекта
cd "$APP_DIR" || {
    echo "❌ Directory $APP_DIR not found!"
    exit 1
}

# Обновляем код из репозитория
# (При запуске через GitHub Actions код уже обновлен, но повторное обновление безопасно)
echo "📥 Fetching latest code..."
git fetch origin
git reset --hard "origin/$BRANCH"
git clean -fd

# Проверяем наличие .env файла
if [ ! -f .env ]; then
    echo "⚠️  Warning: .env file not found!"
    echo "Please create .env file before deployment."
    exit 1
fi

# Останавливаем старые контейнеры
echo "🛑 Stopping old containers..."
docker compose -f docker_compose/storages.yaml -f docker_compose/app.yaml --env-file .env down || true

# Собираем и запускаем контейнеры
echo "🔨 Building and starting containers..."
docker compose -f docker_compose/storages.yaml -f docker_compose/app.yaml --env-file .env up --build -d

# Ждем пока PostgreSQL будет готов
echo "⏳ Waiting for PostgreSQL to be ready..."
sleep 10

# Применяем миграции
echo "📊 Running database migrations..."
docker exec main-app alembic upgrade head || {
    echo "⚠️  Migration failed, but continuing..."
}

# Очищаем старые Docker образы
echo "🧹 Cleaning up old Docker images..."
docker image prune -f

# Проверяем статус контейнеров
echo "✅ Checking container status..."
docker ps --filter "name=main-app" --format "table {{.Names}}\t{{.Status}}"

echo "🎉 Deployment completed successfully!"

