# Users API: app for user registration and auth

## 🔐 Authentication

This API uses [SimpleJWT](https://django-rest-framework-simplejwt.readthedocs.io/en/latest/) for token-based authentication.

---

## Endpoints

| Endpoint                   | Method | Description              |
|----------------------------|--------|--------------------------|
| `/api/register/`      | POST   | Register a new user      |
| `/api/token/`         | POST   | Login and get tokens     |
| `/api/token/refresh/` | POST   | Refresh access token     |

---
