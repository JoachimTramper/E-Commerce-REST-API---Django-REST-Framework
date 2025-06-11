# E-Commerce REST API

An API built with Django REST Framework to support an e-commerce platform. Key features include:

**Robust Cart & Checkout Flow**

- Atomically reserves stock on checkout (`AWAITING_PAYMENT`) with a 10-minute hold.
- Finalizes stock and clears reservations upon successful payment via webhook.

**Secure Webhook Integration**

- Protected by a custom header (`X-Webhook-Key`).
- Accepts JSON payload (`order_id`, `status`) → updates order to `CONFIRMED` and triggers invoice email.

**End-to-End Test Coverage**

- Comprehensive pytest suite: unit, integration, and end-to-end tests, including race-condition scenarios and side-effect mocks.
- CI pipeline (GitHub Actions) with linting, security scans (GitGuardian), test runs, and automated deploys.

**OpenAPI & Swagger-UI Documentation**

- Live “Try it out” API docs with request/response examples.
- Auto-generated TypeScript-Axios SDK in `clients/ts-axios`.

**JWT Authentication with Optional 2FA**

- Email/password login at `POST /api/auth/jwt/create/`.
- Optional TOTP 2FA flows: setup, verify, and disable.
- Token blacklisting for immediate revocation of compromised refresh tokens.

**Out-of-the-Box User Management**

- Djoser-driven registration, activation, password reset, and user endpoints.

**Django Best Practices**

- User signals for welcome emails and TOTP key validation.
- Built-in caching, throttling, permissions, and filter/search support.
- Request/response profiling via Django Silk in development.

**Visual Data Model**

- Generated via `django-extensions`’ `graph_models` (output: `models.dot`; render with Graphviz).

**Periodic Tasks**

- Managed with `django-celery-beat` for scheduling background jobs (e.g. reminders, cleanup).

**Transactional Email via SendGrid**

- All user-facing emails (welcome, password reset, invoices) sent asynchronously through SendGrid with retry logic via Celery.

**Error Monitoring & Audit Trails**

- Integrated with Sentry for real-time error tracking and performance monitoring.
- Django-Simple-History records model changes for full auditability.

**Production-Ready Deployment**

- Docker Compose stack (Django + Gunicorn, PostgreSQL, Redis, Celery, Celery Beat).
- Railway start command: runs `python manage.py migrate --noinput` and `python manage.py collectstatic --noinput`, then launches Gunicorn for zero-downtime deploys.

## Repository Structure

```text
├── clients/ts-axios         # Auto-generated TypeScript-Axios client from OpenAPI schema
├── docs/
│   ├── schema.yml           # OpenAPI 3.0 specification for the API (points to production URL)
│   └── swagger-ui/          # Swagger-UI assets and configuration
└── ecommerce_api/           # Django project code (models, views, serializers, etc.)
    └── settings.py          # Configured for production deployment on Railway
├── Procfile                 # Gunicorn entry point for production
└── requirements.txt         # Python dependencies
```

## Installation & Setup (Development)

1. **Clone the repository**

   ```bash
   git clone https://github.com/joachimtramper/E-Commerce-REST-API---Django-REST-Framework.git
   cd E-Commerce-REST-API---Django-REST-Framework
   ```

2. **Create and activate a virtual environment**

   ```bash
   python -m venv .venv
   # On Windows (PowerShell):
   . .venv/Scripts/activate
   # On Unix/macOS:
   source .venv/bin/activate
   ```

3. **Install dependencies**

   ```bash
   pip install -r requirements.txt
   ```

4. **Apply migrations & run the server**

   ```bash
   python manage.py migrate
   python manage.py runserver
   ```

The development server runs at `http://127.0.0.1:8000/` and the interactive docs are available at `http://127.0.0.1:8000/api/docs/`.

## Live Production

The API is deployed on Railway at:

```
https://web-production-7c555.up.railway.app
```

### Demo Credentials

Use these test credentials to authenticate in Swagger-UI or via the client SDK:

| Email                                       | Password   |
| ------------------------------------------- | ---------- |
| [user@example.com](mailto:user@example.com) | 0XorQ5HMhh |

Obtain a JWT token by POSTing to `/api/auth/jwt/create/`:

```bash
POST https://web-production-7c555.up.railway.app/api/auth/jwt/create/
Content-Type: application/json

{
  "email": "user@example.com",
  "password": "0XorQ5HMhh"
}
```

Include the returned token in the **Authorize** dialog.

## Swagger-UI (Live API Docs)

Interactive API documentation is hosted via GitHub Pages:

[![API Docs](https://img.shields.io/badge/docs-online-blue)](https://joachimtramper.github.io/E-Commerce-REST-API---Django-REST-Framework/swagger-ui/)

Click **Try it out** to execute requests against the production API.

## Client SDK (TypeScript-Axios)

A fully typed TypeScript-Axios client is available in `clients/ts-axios`:

```bash
cd clients/ts-axios
npm install
npm run build
```

### Usage Example

```ts
import { CartApi, Configuration } from "@joachimtramper/ecommerce-api-client";

const api = new CartApi(
  new Configuration({ basePath: "https://web-production-7c555.up.railway.app" })
);

api
  .getCart()
  .then((response) => console.log(response.data))
  .catch(console.error);
```

## Configuration

- **Allowed hosts:** configured in `ecommerce_api/settings.py` to include the Railway domain.
- **Environment variables** (Railway):

  - `DJANGO_SECRET_KEY` (secure random string)
  - `DEBUG=False`
  - `DATABASE_URL` (if using PostgreSQL plugin)

---

## Local Development with Docker

This project includes a complete Docker-based setup to run the full backend stack locally in a production-like environment. Using `docker-compose`, you can launch:

- Django + Gunicorn (`web`)
- Celery worker (`celery`)
- Celery Beat scheduler (`beat`)
- Redis message broker (`redis`)
- PostgreSQL database (`db`)

### Start the stack

```bash
docker-compose up --build
```

This builds and runs all services, exposing the Django API at [http://localhost:8000](http://localhost:8000).

### One-time setup

After building the stack, initialize the database and create a superuser:

```bash
docker exec -it ecommerce-api-web-1 python manage.py migrate
docker exec -it ecommerce-api-web-1 python manage.py createsuperuser
```

### Background tasks

Celery and Celery Beat run in separate containers and process tasks using Redis as a message broker. Tasks like email reminders, daily reports, and cleanup jobs are automatically triggered on schedule.

> Django runs with `DEBUG=True` by default in Docker. Auto-cancellation of orders is skipped during development.

---
