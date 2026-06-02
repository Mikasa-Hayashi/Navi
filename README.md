# Navi

Navi is a full-stack web application with real-time communication, implementing a chat system with an AI companion. The project demonstrates the integration of REST API and WebSocket communication, handling asynchronous events, and maintaining persistent conversation state for users.

## Key Features

- User registration and authentication (JWT)
- Real-time chat via WebSocket (Django Channels)
- Message history storage (PostgreSQL)
- Asynchronous message processing
- Combined REST API and WebSocket architecture in a single application


## Project Structure

- `frontend` — client application (React, routing, API and WebSocket communication)
- `backend` — server-side application (Django, REST API, JWT authentication, WebSocket via Channels)
- `.env.example` — example environment variables for PostgreSQL configuration

## Tech Stack

- **Frontend:** React, Vite — client-side application with routing and state management
- **Backend:** Django, Django REST Framework — API and business logic
- **Аутентификация:** JWT (SimpleJWT)
- **Realtime:** Django Channels + Redis (WebSocket message broker)
- **База данных:** PostgreSQL

## Architecture

- The React client communicates with the server via REST API (Axios)
- Real-time communication is handled via WebSockets (Django Channels)
- Redis is used as a message broker for asynchronous event processing
- Users and messages are stored in PostgreSQL

## Quick Start

1. Install backend dependencies from `requirements.txt`.
2. Configure and run the backend according to `backend/README.md`.
3. Configure and run the frontend according to `frontend/README.md`.
4. Open the frontend in your browser (usually `http://localhost:5173`).

## Running with Docker

1. Ensure Docker Desktop is installed.
2. Copy `.env.example` to `.env` and adjust values if needed.
3. Start containers:

```bash
docker compose up --build
```

After startup:
- frontend: `http://localhost:5173`
- backend: `http://localhost:8000`

Stop services:

```bash
docker compose down
```

Remove everything including PostgreSQL volumes:

```bash
docker compose down -v
```

## API Endpoints

Base API URL: `http://localhost:8000/api/v1/`

Main endpoint groups:

- `users/` — registration, login, logout, token refresh
- `conversations/` — chats and messages
- `companions/` — companion configuration and data

## LLM Configuration

- The free demo mode of the AI companion uses a local Ollama instance.
- Model settings are configured via `.env`:
  - `LLM_PROVIDER=ollama`
  - `LLM_MODEL=qwen2.5:3b-instruct`
  - `LLM_BASE_URL=http://127.0.0.1:11434`
- Detailed setup instructions are available in `backend/README.md`.
