# Hotel Booking System

A Django hotel booking app with customers, hotel owners, and admin dashboards.

## Overview

This project supports:
- hotel browsing and booking
- room and hotel management
- review submission and approval
- role-based customer, owner, and admin access

## Features

- User registration and login
- Hotel and room management
- Booking creation and tracking
- Reviews with approval support
- Simple admin and owner dashboards

## Tech Stack

- Django
- SQLite
- HTML/CSS/JavaScript
- Pillow for image uploads

## Quick Start

```bash
git clone <repository-url>
cd "Hotel booking system"
python -m venv venv
venv\Scripts\activate
pip install django pillow
python manage.py migrate
python manage.py createsuperuser
python manage.py runserver
```

Open `http://localhost:8000` in your browser.

## Structure

- `accounts/` — auth, registration, profile
- `hotels/` — hotel, city, room models and pages
- `bookings/` — booking flow and management
- `reviews/` — guest reviews and approval
- `dashboard/` — owner/admin dashboard pages
- `hotel_project/` — Django settings and URLs

## Main Routes

- `/` — home hotel list
- `/admin/` — Django admin
- `/accounts/register/` — register
- `/accounts/login/` — login
- `/accounts/profile/` — profile
- `/dashboard/` — dashboard

## Notes

- Use `media/` for uploaded hotel, room, and profile images
- For production, disable `DEBUG`, set `ALLOWED_HOSTS`, and use a secure `SECRET_KEY`

## License

MIT License

---

**Last Updated:** May 2026
