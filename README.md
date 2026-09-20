# 🔐 Djoser Advanced — Authentication Service

![Python](https://img.shields.io/badge/Python-3.12-blue?logo=python)
![Django](https://img.shields.io/badge/Django-6.x-092E20?logo=django)
![DRF](https://img.shields.io/badge/Django%20REST%20Framework-3.17-red)
![Djoser](https://img.shields.io/badge/Djoser-2.3-success)
![SimpleJWT](https://img.shields.io/badge/SimpleJWT-JWT-orange)
![Celery](https://img.shields.io/badge/Celery-5.6-37814A?logo=celery&logoColor=white)
![Redis](https://img.shields.io/badge/Redis-broker-DC382D?logo=redis&logoColor=white)
![OpenAPI](https://img.shields.io/badge/OpenAPI-3.x-success)
![SQLite](https://img.shields.io/badge/SQLite-Development-blue?logo=sqlite)

---

# 📖 About

A Django REST Framework authentication API that goes past *configuring* Djoser into *customising* it: replaced serializers, a validators package, an email-change flow built from scratch, real logout through refresh-token blacklisting, and one consistent response envelope across the whole API.

It is the authentication layer later reused, in refined form, in [StoryHub](https://github.com/MohammedAMohsen/storyhub).

---

# ✨ Features

## Accounts

- Custom user model (`AbstractUser`) with **email as the login field**
- Phone numbers stored in **E164** format (`django-phonenumber-field`, default region configurable)
- Avatar, birth date and a one-to-one `Profile` (bio, age) created automatically by a `post_save` signal
- Registration with password retype and **mandatory email activation** (Djoser)

## Validation — a standalone `validators/` package

- Reserved usernames are rejected (`admin`, `root`, `support`, …)
- **Disposable email domains** are rejected at registration
- A **minimum age of 18**, computed from the birth date
- Avatar uploads limited to **2 MB** and an extension allow-list

## Email change — built from scratch

Djoser has no email-change flow, so this project adds one:

1. `POST /auth/users/change-email/` — the new address is validated (format, uniqueness against both live and pending addresses) and stored in `pending_email`; a confirmation link (uid + token) is emailed to the **new** address through Celery
2. `POST /auth/users/confirm-email-change/` — an **unauthenticated** endpoint: the token is verified, a final collision check runs, and only then does `email` change and `pending_email` clear

Nothing changes until the new address proves it can receive mail.

## Sessions

- JWT via SimpleJWT: 60-minute access tokens, 1-day refresh tokens, **refresh rotation with blacklist-after-rotation**
- `POST /auth/users/logout/` — a real logout: the refresh token is blacklisted and answers `205 Reset Content`

## One response shape

- A **global exception handler** turns every error into `{ "success": false, "message": …, "errors": … }`
- A **custom JSON renderer** (`common/renderers.py`) wraps successful responses the same way, skipping `204` and error responses — implemented and ready; enable it by uncommenting `DEFAULT_RENDERER_CLASSES` in `settings.py`

## Storage hygiene

- The previous avatar file is deleted when a new one is uploaded (`pre_save` signal)
- A user's avatar is deleted when the user is deleted (`post_delete` signal)

## Tooling

- Transactional email off the request path: **Celery + Redis**
- OpenAPI 3 schema with **Swagger UI** and **Redoc** (`drf-spectacular`)
- `api.http` — a request collection covering the full flow

---

# 🛠 Tech Stack

| Technology | Role |
|---|---|
| Python 3.12 · Django 6 | Core |
| Django REST Framework 3.17 | API layer |
| Djoser 2.3 | Registration, activation, password flows |
| SimpleJWT 5.5 (+ `token_blacklist`) | JWT issue, refresh, rotation, blacklist |
| Celery 5.6 + Redis | Background email delivery |
| django-phonenumber-field | E164 phone numbers |
| drf-spectacular | OpenAPI schema, Swagger UI, Redoc |
| Pillow | Avatar validation |
| SQLite | Development database |

---

# 📂 Project Structure

```text
djoser_advanced/
├── accounts/
│   ├── models.py          # User (email login, phone, avatar, pending_email) + Profile
│   ├── serializers.py     # Djoser overrides, profile update, email change, logout
│   ├── views.py           # CustomUserViewSet: change-email, confirm-email-change, logout
│   ├── services.py        # Builds the email-change confirmation link
│   ├── tokens.py          # Dedicated token generator for email change
│   ├── tasks.py           # Celery email task
│   ├── signals.py         # Profile creation, avatar cleanup
│   └── validators/        # user.py (username, email, age) · image.py (avatar)
├── common/
│   ├── exceptions.py      # Global exception handler
│   └── renderers.py       # Response-envelope renderer (opt-in)
├── djoser_advanced/       # settings, urls, celery app
├── api.http               # Request collection
└── schema.yml             # Generated OpenAPI schema
```

---

# ⚙ Installation

## 1. Clone the repository

```bash
git clone https://github.com/MohammedAMohsen/djoser-advanced.git
cd djoser-advanced
```

## 2. Create a virtual environment

```bash
python -m venv .venv
source .venv/bin/activate        # Windows: .venv\Scripts\activate
```

## 3. Install requirements

```bash
pip install -r requirements.txt
```

## 4. Environment variables

```bash
cp .env.example .env
```

| Variable | Description |
|---|---|
| `SECRET_KEY` | Django secret key |
| `EMAIL_USER` · `EMAIL_PASS` | Gmail account and app password used for SMTP |
| `FRONTEND_URL` | Host the activation and email-change links point at (e.g. `localhost:5173`) |

## 5. Migrate and run

```bash
python manage.py migrate
python manage.py createsuperuser
python manage.py runserver
```

Activation and email-change mails are sent by Celery, so start a worker in a second terminal (Redis must be running on `127.0.0.1:6379`):

```bash
celery -A djoser_advanced worker -l info
```

---

# 🔗 API Overview

Interactive documentation: `/api/schema/swagger-ui/` and `/api/schema/redoc/`.

| Method | Endpoint | Description |
|---|---|---|
| `POST` | `/auth/users/` | Register (password retype, custom validation, activation email) |
| `POST` | `/auth/users/activation/` | Activate from the emailed link |
| `POST` | `/auth/jwt/create/` | Sign in — access + refresh tokens |
| `POST` | `/auth/jwt/refresh/` | Rotate the refresh token |
| `GET` | `/auth/users/me/` | Current user with profile |
| `PATCH` | `/auth/users/me/` | Update profile fields, avatar, phone, birth date |
| `POST` | `/auth/users/change-email/` | Start the email-change flow |
| `POST` | `/auth/users/confirm-email-change/` | Confirm from the link sent to the new address |
| `POST` | `/auth/users/logout/` | Blacklist the refresh token |
| `POST` | `/auth/users/reset_password/` · `…/reset_password_confirm/` | Password reset (Djoser) |
| `POST` | `/auth/users/set_password/` | Change password (retype required) |

Authorization header: `JWT <access token>`.

---

# 🚀 Future Improvements

- Automated tests for the validators and the email-change flow
- Enable the response-envelope renderer by default
- Environment-driven Redis and email settings
- A React client (see [django-react-authentication](https://github.com/MohammedAMohsen/django-react-authentication))

---

# 📄 License

MIT
