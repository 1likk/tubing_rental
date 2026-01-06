# Деплой на Render.com

## Подготовка

1. Создайте аккаунт на [Render.com](https://render.com)
2. Подключите свой GitHub репозиторий

## Автоматический деплой (рекомендуется)

### Шаг 1: Загрузите код на GitHub

```bash
git init
git add .
git commit -m "Initial commit"
git branch -M main
git remote add origin <your-repo-url>
git push -u origin main
```

### Шаг 2: Создайте Blueprint на Render

1. Войдите в Render.com
2. Нажмите **New** → **Blueprint**
3. Выберите ваш GitHub репозиторий
4. Render автоматически обнаружит `render.yaml` и создаст:
   - PostgreSQL базу данных
   - Web service с Django приложением

### Шаг 3: Настройте переменные окружения

Render автоматически создаст большинство переменных, но нужно добавить:

1. Перейдите в Dashboard → ваш сервис → **Environment**
2. Добавьте:
   ```
   ALLOWED_HOSTS = your-app-name.onrender.com
   ```

### Шаг 4: Деплой

Render автоматически:
- Установит зависимости из `requirements.txt`
- Выполнит `build.sh` (collectstatic и migrate)
- Запустит приложение через Gunicorn

## Ручной деплой

### Создание PostgreSQL базы

1. **New** → **PostgreSQL**
2. Name: `tubing-rental-db`
3. Database: `tubing_rental`
4. User: `tubing_rental`
5. Region: выберите ближайший
6. **Create Database**

После создания скопируйте **Internal Database URL**

### Создание Web Service

1. **New** → **Web Service**
2. Выберите репозиторий или **Public Git repository**
3. Настройки:
   - **Name**: `tubing-rental`
   - **Region**: тот же, что и БД
   - **Branch**: `main`
   - **Runtime**: `Python 3`
   - **Build Command**: `./build.sh`
   - **Start Command**: `gunicorn tubing_rental.wsgi:application`

4. **Environment Variables**:
   ```
   DATABASE_URL = <Internal Database URL из шага выше>
   SECRET_KEY = <сгенерируйте новый через Django>
   DEBUG = False
   ALLOWED_HOSTS = your-app-name.onrender.com
   ```

5. Нажмите **Create Web Service**

## После деплоя

### Создание суперпользователя

1. Перейдите в Dashboard → ваш сервис → **Shell**
2. Выполните:
   ```bash
   python manage.py createsuperuser
   ```

### Добавление тюбингов

1. Откройте `https://your-app-name.onrender.com/admin`
2. Войдите с учеткой суперпользователя
3. Добавьте тюбинги

## Обновление приложения

### Автоматическое

При пуше в GitHub, Render автоматически задеплоит изменения:

```bash
git add .
git commit -m "Update description"
git push
```

### Ручное

В Dashboard → ваш сервис → **Manual Deploy** → **Deploy latest commit**

## Мониторинг

- **Logs**: Dashboard → сервис → **Logs**
- **Metrics**: Dashboard → сервис → **Metrics**
- **Health**: автоматические health checks

## Важные примечания

### Бесплатный план (Free Tier):
- ✅ 750 часов/месяц Web Service
- ⚠️ Сервис засыпает после 15 минут неактивности
- ⚠️ Первый запрос после сна: 30-50 секунд (cold start)
- ⚠️ База данных **удаляется через 90 дней**
- 💡 Решение: делайте backup каждую неделю с помощью `backup.sh`

#### Как сделать backup БД:
```bash
# 1. Получите DATABASE_URL из Render Dashboard
# 2. Отредактируйте backup.sh, вставьте ваш DATABASE_URL
# 3. Запустите:
./backup.sh

# Для автоматического backup (macOS/Linux):
crontab -e
# Добавьте строку (каждое воскресенье в 3:00):
0 3 * * 0 /path/to/tubing_rental/backup.sh
```

#### Восстановление из backup:
```bash
# На локальной машине:
psql $DATABASE_URL < backups/backup_2026-01-06_15-30-00.sql
```

### Платный план (Starter - $7/месяц):
- ✅ Сервис всегда активен (нет cold start)
- ✅ Больше ресурсов (512 MB → 2 GB RAM)
- ✅ База данных не удаляется
- ✅ Приоритетная поддержка

Рекомендуется переходить на платный план, когда:
- У вас более 10 активных пользователей в день
- Нужна стабильная работа без задержек
- Важна сохранность данных

1. **Free tier**:
   - Сервис засыпает после 15 минут неактивности
   - Первый запрос может занять 30-50 секунд
   - База данных удаляется через 90 дней

2. **Paid tier** ($7/мес):
   - Сервис всегда активен
   - Больше ресурсов
   - База данных не удаляется

3. **Custom domain**:
   - Можно подключить свой домен в настройках сервиса

## Как проверить проект локально перед деплоем

Перед деплоем на Render убедитесь, что всё работает локально:

```bash
# 1. Установите зависимости
pip install -r requirements.txt

# 2. Создайте .env файл (если ещё не создан)
cp .env.example .env

# 3. Отредактируйте .env, добавьте свои данные
nano .env

# 4. Примените миграции
python manage.py migrate

# 5. Соберите статические файлы
python manage.py collectstatic --no-input

# 6. Создайте суперпользователя (если нужно)
python manage.py createsuperuser

# 7. Запустите сервер
python manage.py runserver

# 8. Проверьте в браузере:
# http://localhost:8000 - главная
# http://localhost:8000/admin - админка
```

Если всё работает локально, можно деплоить на Render.

## Troubleshooting

### Ошибка "Failed to deploy"

Если деплой не удался, проверьте следующее:

1. **Логи сборки на Render**:
   - Dashboard → ваш сервис → **Logs**
   - Ищите строки с ошибками (обычно красного цвета)

2. **Проблемы с зависимостями**:
   ```bash
   # Проверьте локально, что все зависимости устанавливаются:
   pip install -r requirements.txt
   ```

3. **Проблемы с миграциями**:
   ```bash
   # Проверьте локально, что миграции применяются:
   python manage.py migrate
   ```

4. **Проблемы со статическими файлами**:
   ```bash
   # Проверьте локально:
   python manage.py collectstatic --no-input
   ```

5. **Версия Python**:
   - Убедитесь, что `runtime.txt` содержит поддерживаемую версию
   - Render поддерживает Python 3.8+
   - Текущая версия в проекте: 3.12.0

6. **Регион базы данных**:
   - БД и web service должны быть в одном регионе
   - В `render.yaml` оба используют `region: oregon`

### Ошибка при сборке

Проверьте логи сборки:
```bash
./build.sh
```

### Ошибка подключения к БД

Убедитесь, что `DATABASE_URL` правильный и сервис в том же регионе, что и БД

### Static files не загружаются

Проверьте, что выполнилась команда:
```bash
python manage.py collectstatic --no-input
```

### Ошибка ALLOWED_HOSTS

Добавьте домен Render в переменную окружения:
```
ALLOWED_HOSTS = your-app-name.onrender.com
```

## Полезные ссылки

- [Render Django Guide](https://render.com/docs/deploy-django)
- [Render Docs](https://render.com/docs)
- [Django Deployment Checklist](https://docs.djangoproject.com/en/stable/howto/deployment/checklist/)
