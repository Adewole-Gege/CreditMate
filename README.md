# 🏦 Business Credit Scoring API

A Django REST API for managing businesses and their credit scoring process, with user authentication, ownership-based permissions, and secure JWT login.

---

## 🚀 Features

- User registration and JWT authentication
- CRUD operations on Business records
- Ownership-based permissions: users can only manage their own businesses
- Admins have full access to all records
- Search and filter businesses
- Token-based authentication (SimpleJWT)

---

## 📦 Tech Stack

- Python 3.x
- Django
- Django REST Framework
- SimpleJWT (for authentication)
- django-filter (for search & filtering)

---

## Users API: app for user registration and auth

### 🔐 Authentication

This API uses [SimpleJWT](https://django-rest-framework-simplejwt.readthedocs.io/en/latest/) for token-based authentication.

---

### Endpoints

| Endpoint                   | Method | Description              |
|----------------------------|--------|--------------------------|
| `/api/register/`      | POST   | Register a new user      |
| `/api/token/`         | POST   | Login and get tokens     |
| `/api/token/refresh/` | POST   | Refresh access token     |

---

## 🏢 Business API: app for business models and views

### Base URL: `/api/businesses/`

| Endpoint                 | Method | Description            |
|--------------------------|--------|------------------------|
| `/api/businesses/`       | GET    | List user’s businesses |
| `/api/businesses/`       | POST   | Create new business    |
| `/api/businesses/<id>/`  | GET    | Retrieve a business    |
| `/api/businesses/<id>/`  | PUT    | Full update (admin/owner only) |
| `/api/businesses/<id>/`  | PATCH  | Partial update         |
| `/api/businesses/<id>/`  | DELETE | Delete business        |

---

## 🔍 Filtering & Search

- Search by `name`, `industry`, or `city`:
/api/businesses/?search=tech

- Filter by country or number of employees:
/api/businesses/?country=USA&number_of_employees=50

---

## 🛡️ Permissions

| Role      | Action                                |
|-----------|----------------------------------------|
| Admin     | Full access to all businesses          |
| User      | Can only access their own businesses   |
| Anonymous | Can register and log in only           |

---

## 🛠️ Setup

1. **Clone the repo**

```bash
    git clone https://github.com/Adewole-Gege/CreditMate.git
    cd CreditMate/
```

2. **Create a virtual environment**

```bash
    python3 -m venv .env

    # Activate the virtual environment
    source .env/bin/activate
```

3. **Install Dependencies**

```bash
    pip install -r requirements.txt
```

4. **Run migrations**

```bash
    python manage.py makemigrations
    python manage.py migrate
```

5. **Create superuser**

```bash
    python manage.py createsuperuser
```

6. **Run the server**

```bash
    python manage.py runserver
```
