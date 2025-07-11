# 🏢 Business API: app for business models and views

## Base URL: `/api/businesses/`

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
