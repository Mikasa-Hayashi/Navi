# Backend (Navi)

Серверная часть проекта на Django + Django REST Framework.

## Требования

- Python 3.11+ (рекомендуется)
- PostgreSQL
- Redis (для WebSocket/Channels)

## Установка

1. Создайте и активируйте виртуальное окружение:

```bash
python -m venv .venv
.venv\Scripts\activate
```

2. Установите зависимости:

```bash
pip install -r ../requirements.txt
```

Файл зависимостей находится в корне проекта: `requirements.txt`.

## Настройка окружения

Создайте файл `.env` в корне проекта (рядом с `frontend` и `backend`) по примеру `.env.example`:

```env
PG_NAME=your_db_name
PG_USER=your_db_user
PG_PASSWORD=your_db_password
PG_HOST=localhost
PG_PORT=5432
```

## Миграции

Из папки `backend` выполните:

```bash
python manage.py makemigrations
python manage.py migrate
```

## Запуск сервера

```bash
python manage.py runserver
```

Сервер будет доступен на `http://localhost:8000`.

## Основные эндпоинты

- `POST /api/token/` - получение JWT
- `POST /api/v1/users/register/` - регистрация
- `POST /api/v1/users/login/` - вход
- `POST /api/v1/users/token/refresh` - обновление access-токена
- `GET /api/v1/conversations/` - список диалогов
- `GET /api/v1/companions/` - список компаньонов

## WebSocket

Для чата используется endpoint:

- `ws://localhost:8000/ws/chat/<conversation_id>/`

Убедитесь, что Redis запущен на `127.0.0.1:6379`, иначе realtime-функции не будут работать.
