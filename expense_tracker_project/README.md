# Expense Tracker Backend

## Features
- JWT Authentication
- Add, list, and analyze expenses
- Filters by date range
- Analytics (total, category-wise, trends)

## Setup Instructions
```bash
pip install -r requirements.txt
python manage.py makemigrations
python manage.py migrate
python manage.py createsuperuser
python manage.py runserver
```

## API Endpoints
- `POST /api/login/` – Login to get JWT token
- `POST /api/expenses/` – Create expense (auth required)
- `GET /api/expenses/?start_date=YYYY-MM-DD&end_date=YYYY-MM-DD` – Filtered list
- `GET /api/expenses/analytics/` – Expense insights
