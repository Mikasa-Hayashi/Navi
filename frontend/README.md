# Frontend (Navi)

Клиентская часть проекта на React + Vite.

## Требования

- Node.js 18+
- npm

## Установка

```bash
npm install
```

## Запуск в режиме разработки

```bash
npm run dev
```

или

```bash
npm run dev -- --host
```

По умолчанию приложение доступно на `http://localhost:5173`.

## Сборка

```bash
npm run build
```

## Предпросмотр production-сборки

```bash
npm run preview
```

## Линтинг

```bash
npm run lint
```

## E2E тесты (Playwright)

1. Установите зависимости:

```bash
npm install
```

2. Один раз установите браузер Chromium для Playwright:

```bash
npx playwright install chromium
```

3. Запустите E2E тесты:

```bash
npm run test:e2e
```

Дополнительно:
- UI-режим: `npm run test:e2e:ui`
- Headed-режим: `npm run test:e2e:headed`
- HTML-отчет: `npm run test:e2e:report`

## Взаимодействие с бэкендом

- Базовый URL API задан в `src/api/axios.js`: `http://localhost:8000`
- Основные API-маршруты:
  - `/api/v1/users/`
  - `/api/v1/conversations/`
  - `/api/v1/companions/`
- WebSocket-чат использует адрес вида: `ws://localhost:8000/ws/chat/<conversation_id>/`

Перед запуском фронтенда убедитесь, что сервер из `backend` запущен.
