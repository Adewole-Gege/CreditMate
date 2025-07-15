# CreditMate: a business credit scoring and risk assessment API

CreditMate provides a comprehensive solution for small and medium enterprises (SMEs) to facilitate onboarding, financial data submission, credit scoring, and risk classification.

---

## Table of Contents

- [Introduction](#creditmate-a-business-credit-scoring-and-risk-assessment-api)
- [Table of Contents](#table-of-contents)
- [Features](#-features)
- [Tech Stack](#-tech-stack)
- [Setup](#️-setup)
- [Users API](#users-api-app-for-user-registration-and-auth)
  - [Examples](#examples-for-user)
- [Business API](#-business-api-app-for-business-models-and-views)
  - [Examples](#examples-for-business)
- [Ingestion API](#ingestion-api-app-for-uploading-and-downloading-financial-statements)
  - [Examples](#examples-for-ingestion)
- [Credit Scoring](#credit-scoring-and-risk-assessment-api-calculates-the-credit-score-of-the-business)
  - [Examples](#examples-for-credit-scoring-and-risk-assessment)
- [Alternative for testing endpoints](#alternative-for-testing-endpoints)

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

---

## Users API: app for user registration and auth

### 🔐 Authentication

This API uses [SimpleJWT](https://django-rest-framework-simplejwt.readthedocs.io/en/latest/) for token-based authentication.

---

### Endpoints for User app

| Endpoint                   | Method | Description              |
|----------------------------|--------|--------------------------|
| `/api/register/`      | POST   | Register a new user      |
| `/api/token/`         | POST   | Login and get tokens     |
| `/api/token/refresh/` | POST   | Refresh access token     |

### Examples for User

1. **Register a new user**

```bash
    curl --location 'http://localhost:8000/api/register/' \
    --header 'Content-Type: application/json' \
    --data-raw '{
        "email": "testuser@example.com",
        "first_name": "Test",
        "last_name": "User",
        "password": "TestPassword123"
    }'
```

Returns:

```bash
    {
        "email": "testuser@example.com",
        "first_name": "Test",
        "last_name": "User"
    }
```

2. **Login and get tokens**

```bash
    curl --location 'http://localhost:8000/api/token/' \
    --header 'Content-Type: application/json' \
    --data-raw '{
        "email": "testuser@example.com",
        "password": "TestPassword123"
    }'
```

Returns:

```json
{
    "refresh": "REFRESH_TOKEN",
    "access": "ACCESS_TOKEN"
}

# Example
{
    "refresh": "eyJhbGciOiJIUzI1NiIsInR5cCI6IkpXVCJ9.eyJ0b2tlbl90eXBlIjoicmVmcmVzaCIsImV4cCI6MTc1MjU3NjQzMSwiaWF0IjoxNzUyNDkwMDMxLCJqdGkiOiI5OTdjOWM4YWI2YTY0ZTVlYjJlZWMxOGRjOThjZThhOSIsInVzZXJfaWQiOjF9.mj1Wp29O5o62Zj4nGcUAldDpcef5garRYo4cavTdq0s",
    "access": "eyJhbGciOiJIUzI1NiIsInR5cCI6IkpXVCJ9.eyJ0b2tlbl90eXBlIjoiYWNjZXNzIiwiZXhwIjoxNzUyNDkwOTMxLCJpYXQiOjE3NTI0OTAwMzEsImp0aSI6IjczMjI2ODc1N2VjOTQ4ODRhZGE5YWE4YTc5ZmU4ZmU3IiwidXNlcl9pZCI6MX0.855em4T_1K5NitetpTGewDG5jp_OaNrAIqmU00_qB7Q"
}

# NB: Each request return a different token pair. Yours will be different
```

3. **Refresh access token**

```bash
curl --location 'http://localhost:8000/api/token/refresh/' \
--header 'Content-Type: application/json' \
--data '{
        "refresh": "eyJhbGciOiJIUzI1NiIsInR5cCI6IkpXVCJ9.eyJ0b2tlbl90eXBlIjoicmVmcmVzaCIsImV4cCI6MTc1MjU3NjQzMSwiaWF0IjoxNzUyNDkwMDMxLCJqdGkiOiI5OTdjOWM4YWI2YTY0ZTVlYjJlZWMxOGRjOThjZThhOSIsInVzZXJfaWQiOjF9.mj1Wp29O5o62Zj4nGcUAldDpcef5garRYo4cavTdq0s"
      }'

# Returns a new token pair same as when you login
```

---

## 🏢 Business API: app for business models and views

### Endpoints for Business app

| Endpoint                 | Method | Description            |
|--------------------------|--------|------------------------|
| `/api/businesses/`       | GET    | List user’s businesses |
| `/api/businesses/`       | POST   | Create new business    |
| `/api/businesses/<id>/`  | GET    | Retrieve a business    |
| `/api/businesses/<id>/`  | PUT    | Full update (admin/owner only) |
| `/api/businesses/<id>/`  | DELETE | Delete business        |

### Examples for Business

1. **Create a Business**

```bash
curl --location 'http://localhost:8000/api/businesses/' \
--header 'Authorization: Bearer ACCESS_TOKEN' \
--header 'Content-Type: application/json' \
--data-raw '{
        "name": "TechNo Inc.",
        "registration_number": "TN-2027",
        "tax_id": "TIN-789456125",
        "industry": "Technology",
        "date_founded": "2020-01-01",
        "website": "https://technov.example.com",
        "email": "contact@technov.com",
        "phone_number": "+1234567891",
        "address": "43 Silicon Street",
        "country": "USA",
        "city": "San Francisco"
      }'
# NB: You must be logged in to create a business
```

2. **List User's Buinesses**

```bash
curl --location 'http://localhost:8000/api/businesses/' \
--header 'Authorization: Bearer ACCESS_TOKEN'
```

3. **Retrieve a Buiness**

```bash
curl --location 'http://localhost:8000/api/businesses/<int:business_id>/' \
--header 'Authorization: Bearer ACCESS_TOKEN'
```

4. **Update a Business**

```bash
curl --location --request PUT 'http://localhost:8000/api/businesses/<int:business_id>/' \
--header 'Authorization: Bearer ACCESS_TOKEN' \
--header 'Content-Type: application/json' \
--data-raw '{
        "name": "TechNova International",
        "registration_number": "TN-2025",
        "tax_id": "TIN-789456123",
        "industry": "Tech & AI",
        "date_founded": "2020-01-01",
        "website": "https://technova.ai",
        "email": "info@technova.ai",
        "phone_number": "+1987654321",
        "address": "42 Innovation Way",
        "country": "USA",
        "city": "San Jose"
      }'
```

5. **Delete a Business**

```bash
curl --location --request DELETE 'http://localhost:8000/api/businesses/<int:business_id>/' \
--header 'Authorization: Bearer ACCESS_TOKEN'
```

---

### 🔍 Filtering & Search

- Search by `name`, `industry`, or `city`:
/api/businesses/?search=tech

- Filter by country or number of employees:
/api/businesses/?country=USA&number_of_employees=50

---

## Ingestion API: app for uploading and downloading financial statements

### Endpoints for Ingestion app

| Endpoint                 | Method | Description            |
|--------------------------|--------|------------------------|
| `/api/upload-statement/`       | POST   | Upload financial statement    |
| `/api/download-statement/<int:statement_id>`       | GET    | Download financial statement |

### Examples for Ingestion

***You can get your OPEN ROUTER API KEY by visiting and creating an account*** [here](https://openrouter.ai/)

1. Uploading financial statement

```bash
curl --location 'http://localhost:8000/api/upload-statement/<int:business_id>/' \
--header 'API_KEY: OPEN_ROUTER_API_KEY' \
--header 'Authorization: ACCESS_TOKEN' \
--header 'Content-Type: multipart/form'
--form 'file=PATH_TO_THE_FINANCIAL_STATEMENT"'
```

2. Downloading financial statement

```bash
curl --location 'http://localhost:8000/api/download-statement/<int:statement_id>/' --request GET \
--header 'Content-Type: application/json' \
--header 'Authorization: Bearer ACCESS_TOKEN' \
```

---

## Credit Scoring and Risk Assessment API: calculates the credit score of the business

### Endpoints for the Credit Scoring app

| Endpoint                 | Method | Description            |
|--------------------------|--------|------------------------|
| `/api/score-from-statement/<int:business_id>`       | GET    | Get the credit score of a business |
| `/api/risk/<int:business_id>`       | GET    | Returns risk level only for a given business |

### Examples for credit scoring and risk assessment

1. Getting the credit score

```bash
curl --location 'http://localhost:8000/api/score-from-statement/<int:business_id>/' --request GET \
--header 'Content-Type: application/json' \
--header 'Authorization: Bearer ACCESS_TOKEN' \
```

2. Getting the risk level assessment for a business

```bash
curl --location 'http://localhost:8000/api/risk/<int:business_id>/' --request GET \
--header 'Content-Type: application/json' \
--header 'Authorization: Bearer ACCESS_TOKEN' \
```

---

## Alternative for testing endpoints

You can use the [postman collection](CreditMate.postman_collection.json) provided in the repo to test the endpoints.

Drag (`CreditMate.postman_collection.json`) and drop it in postman and you can begin testing.

---

## 🛡️ Permissions

| Role      | Action                                |
|-----------|----------------------------------------|
| Admin     | Full access to all businesses          |
| User      | Can only access their own businesses   |
