# Django Expense Management System

A complete, professional full-stack expense management system built with Django, SQLite, Bootstrap 5, and Python 3.

## Features

- ✅ User Authentication (Register, Login, Logout)
- ✅ Dashboard with Income/Expense Summary
- ✅ Expense Management (Add, Edit, Delete)
- ✅ Income Management (Add, Edit, Delete)
- ✅ Category Management
- ✅ Filtering and Search
- ✅ Monthly Reports
- ✅ Responsive Bootstrap 5 UI
- ✅ Pagination
- ✅ Export to CSV
- ✅ Delete Confirmation Modals

## Installation & Setup

### Prerequisites
- Python 3.8 or higher
- pip

### Installation Steps

1. **Navigate to project directory**
```bash
cd expense_management_project
```

2. **Install Django** (if not already installed)
```bash
pip install django
```

3. **Run migrations**
```bash
python manage.py makemigrations
python manage.py migrate
```

4. **Create a superuser** (optional, for admin access)
```bash
python manage.py createsuperuser
```

5. **Run the development server**
```bash
python manage.py runserver
```

6. **Access the application**
- Open your browser and go to: `http://127.0.0.1:8000/`
- Register a new account or login

## Project Structure

```
expense_management_project/
│
├── manage.py
├── db.sqlite3 (created after migrations)
├── README.md
│
├── expense_management_project/
│   ├── __init__.py
│   ├── settings.py
│   ├── urls.py
│   ├── wsgi.py
│   └── asgi.py
│
├── expenses/
│   ├── __init__.py
│   ├── admin.py
│   ├── apps.py
│   ├── models.py
│   ├── views.py
│   ├── urls.py
│   ├── forms.py
│   └── migrations/
│
├── templates/
│   ├── base.html
│   ├── registration/
│   │   ├── login.html
│   │   └── register.html
│   └── expenses/
│       ├── dashboard.html
│       ├── expense_list.html
│       ├── expense_form.html
│       ├── income_list.html
│       ├── income_form.html
│       ├── category_list.html
│       ├── category_form.html
│       └── reports.html
│
└── static/
    ├── css/
    │   └── style.css
    └── js/
        └── main.js
```

## Features Guide

### Dashboard
- View total income, expenses, and current balance
- See recent transactions
- Quick access to all features

### Expense Management
- Add new expenses with category, amount, date, and description
- Edit existing expenses
- Delete expenses with confirmation
- Filter by category and date range
- Search by title

### Income Management
- Add income sources
- Edit and delete income records
- Track all income sources

### Category Management
- Create custom expense categories
- Edit category names
- Delete unused categories

### Reports
- Monthly expense summary
- Category-wise breakdown
- Income vs Expense comparison
- Export data to CSV

## Technologies Used

- **Backend**: Django 4.2+
- **Database**: SQLite3
- **Frontend**: HTML5, CSS3, Bootstrap 5
- **JavaScript**: Vanilla JS

## Security Features

- CSRF Protection on all forms
- Login required decorators
- Password hashing
- User-specific data isolation
- SQL injection prevention via Django ORM

## Default Categories

When you register, the system automatically creates these default categories:
- Food
- Travel
- Shopping
- Bills
- Others

You can add, edit, or delete categories as needed.

## Support

For issues or questions, please check:
- Django Documentation: https://docs.djangoproject.com/
- Bootstrap Documentation: https://getbootstrap.com/docs/

## License

This project is provided as-is for educational and personal use.
