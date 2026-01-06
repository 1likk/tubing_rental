#!/bin/bash
# Скрипт для backup базы данных с Render.com

# Замените на ваши данные из Render Dashboard
DATABASE_URL="your-database-url-from-render"
BACKUP_DIR="./backups"
DATE=$(date +%Y-%m-%d_%H-%M-%S)

# Создаем директорию для бэкапов
mkdir -p $BACKUP_DIR

# Делаем дамп базы данных
pg_dump $DATABASE_URL > $BACKUP_DIR/backup_$DATE.sql

echo "Backup создан: $BACKUP_DIR/backup_$DATE.sql"

# Удаляем старые бэкапы (оставляем последние 10)
ls -t $BACKUP_DIR/backup_*.sql | tail -n +11 | xargs rm -f

echo "Старые бэкапы удалены"
