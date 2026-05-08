# Hotel Booking System

A comprehensive Django-based hotel booking management system with support for multiple user roles, real-time bookings, and administrative features.

## 📋 Project Overview

The Hotel Booking System is a full-featured web application that allows users to:
- **Customers**: Browse hotels, make bookings, leave reviews, and manage their reservations
- **Hotel Owners**: Manage their hotels, rooms, pricing, and view bookings
- **Administrators**: Oversee the entire platform, manage users, and system settings

## 🎯 Features

### User Management
- User registration and authentication
- Three user roles: Customer, Hotel Owner, Administrator
- User profiles with bio, phone, and profile photo
- Role-based access control

### Hotel Management
- Create, update, and delete hotels
- Hotel details: name, address, description, star ratings (1-5 stars)
- City categorization and filtering
- Hotel amenities management
- Contact information (phone, email)
- Hotel thumbnail and multiple images
- Dynamic pricing per night

### Room Management
- Room creation and management within hotels
- Room types (Single, Double, Suite, Deluxe)
- Room capacity and availability tracking
- Room pricing
- Room images and descriptions

### Booking System
- Browse and search available hotels and rooms
- Create reservations with date selection
- Booking status tracking (Pending, Confirmed, Cancelled, Completed)
- Unique booking reference (ETH-XXXX format)
- Guest count management
- Special requests handling
- Automatic price calculation based on number of nights

### Reviews & Ratings
- Guest reviews after booking completion
- Star ratings for hotels
- Review approval workflow
- Average rating calculation
- Review management for administrators

### Dashboard
- **Admin Dashboard**: System overview, user management, hotel management
- **Hotel Owner Dashboard**: Manage owned hotels, rooms, and bookings
- **Customer Dashboard**: View bookings, reviews, and account settings

## 🛠️ Tech Stack

- **Backend**: Django 3.2+
- **Database**: SQLite (default, configurable to PostgreSQL/MySQL)
- **Frontend**: HTML5, CSS3, JavaScript
- **Authentication**: Django built-in authentication
- **Forms**: Django Forms
- **Media Handling**: Django media files for images

## 📁 Project Structure

```
hotel_booking_system/
├── accounts/           # User authentication and profiles
│   ├── models.py      # UserProfile model
│   ├── views.py       # Login, register, profile views
│   ├── forms.py       # User forms
│   └── urls.py        # Account routes
├── hotels/            # Hotel management
│   ├── models.py      # Hotel, City, Room models
│   ├── views.py       # Hotel listing, detail views
│   ├── forms.py       # Hotel forms
│   └── urls.py        # Hotel routes
├── bookings/          # Booking management
│   ├── models.py      # Booking model with reference generation
│   ├── views.py       # Create, update, cancel booking
│   ├── forms.py       # Booking forms
│   └── urls.py        # Booking routes
├── reviews/           # Review system
│   ├── models.py      # Review model
│   ├── views.py       # Review creation and management
│   └── urls.py        # Review routes
├── dashboard/         # Admin and owner dashboards
│   ├── views.py       # Dashboard views (Admin, Owner)
│   └── urls.py        # Dashboard routes
├── hotel_project/     # Project configuration
│   ├── settings.py    # Django settings
│   ├── urls.py        # Main URL configuration
│   └── wsgi.py        # WSGI configuration
├── templates/         # HTML templates
│   ├── base.html      # Base template
│   ├── accounts/      # Account templates
│   ├── hotels/        # Hotel templates
│   ├── bookings/      # Booking templates
│   ├── dashboard/     # Dashboard templates
│   └── reviews/       # Review templates (if exists)
├── static/            # CSS, JavaScript, images
│   ├── css/
│   ├── js/
│   └── images/
├── media/             # User-uploaded files
│   ├── hotel_images/
│   └── profiles/
├── manage.py          # Django management script
└── db.sqlite3         # Database file
```

## 🚀 Installation & Setup

### Prerequisites
- Python 3.8 or higher
- pip (Python package manager)
- Virtual environment (recommended)

### 1. Clone the Repository
```bash
git clone <repository-url>
cd "Hotel booking system"
```

### 2. Create Virtual Environment
```bash
# On Windows
python -m venv venv
venv\Scripts\activate

# On macOS/Linux
python3 -m venv venv
source venv/bin/activate
```

### 3. Install Dependencies
```bash
pip install django pillow
```

### 4. Apply Migrations
```bash
python manage.py migrate
```

### 5. Create Superuser (Admin Account)
```bash
python manage.py createsuperuser
```

### 6. Run Development Server
```bash
python manage.py runserver
```

The application will be available at `http://localhost:8000`

## 📝 Database Models

### UserProfile
- `user` - ForeignKey to Django User
- `role` - Choice field (customer, hotel_owner, admin)
- `phone` - Contact number
- `profile_photo` - Profile picture
- `bio` - User biography

### Hotel
- `name` - Hotel name
- `city` - ForeignKey to City
- `address` - Street address
- `description` - Detailed description
- `star_rating` - 1-5 star rating
- `price_per_night` - Base price
- `owner` - ForeignKey to User
- `amenities` - Comma-separated amenities list
- `thumbnail` - Hotel image
- `is_active` - Active/inactive status

### Room
- `hotel` - ForeignKey to Hotel
- `name` - Room name/number
- `room_type` - Type of room
- `capacity` - Number of guests
- `price_per_night` - Room-specific price
- `description` - Room details
- `image` - Room photo
- `is_available` - Availability status

### Booking
- `booking_ref` - Unique reference (auto-generated)
- `user` - ForeignKey to User
- `room` - ForeignKey to Room
- `check_in` - Check-in date
- `check_out` - Check-out date
- `guests` - Number of guests
- `total_price` - Calculated price
- `status` - Booking status
- `special_requests` - Additional requests

### Review
- `user` - ForeignKey to User
- `hotel` - ForeignKey to Hotel
- `rating` - Star rating
- `comment` - Review text
- `is_approved` - Moderation flag

## 👥 User Roles & Permissions

### Customer
- Browse hotels and rooms
- Create and manage bookings
- Submit reviews
- View booking history
- Update profile

### Hotel Owner
- Add and manage hotels
- Manage rooms within hotels
- View bookings for owned hotels
- Update pricing
- Access hotel dashboard

### Administrator
- Full system access
- Manage users and roles
- Moderate reviews
- View all bookings
- System settings

## 🔗 Main URL Routes

| Route | Purpose |
|-------|---------|
| `/` | Home page - Hotel listing |
| `/admin/` | Django admin panel |
| `/accounts/register/` | User registration |
| `/accounts/login/` | User login |
| `/accounts/profile/` | User profile |
| `/bookings/create/<room_id>/` | Create booking |
| `/bookings/my-bookings/` | View user bookings |
| `/reviews/` | Reviews management |
| `/dashboard/` | User dashboard |

## 💾 Management Commands

### Seed Sample Data
```bash
python manage.py seed_data
```

### Create Superuser
```bash
python manage.py createsuperuser
```

## 📸 Media Files

The system supports uploading:
- **Hotel Images** - Thumbnails and gallery images stored in `media/hotel_images/`
- **Room Images** - Room photos in `media/hotels/`
- **Profile Photos** - User profile pictures in `media/profiles/`

## 🔒 Security Notes

⚠️ **For Production Deployment:**
- Change `SECRET_KEY` in `settings.py`
- Set `DEBUG = False`
- Configure `ALLOWED_HOSTS` with your domain
- Use environment variables for sensitive settings
- Configure proper database (PostgreSQL/MySQL)
- Set up HTTPS/SSL
- Configure email backend for notifications

## 📱 Browser Compatibility

- Chrome (latest)
- Firefox (latest)
- Safari (latest)
- Edge (latest)

## 🐛 Troubleshooting

### Static files not loading
```bash
python manage.py collectstatic
```

### Database errors
```bash
python manage.py migrate
```

### Module import errors
```bash
pip install -r requirements.txt
```

## 📄 License

This project is open source and available under the MIT License.

## 👨‍💻 Development

### Adding a New App
1. Create app: `python manage.py startapp <app_name>`
2. Add to `INSTALLED_APPS` in `settings.py`
3. Create models, views, and URLs
4. Run migrations: `python manage.py makemigrations` then `python manage.py migrate`

### Database Migrations
```bash
# Create migrations
python manage.py makemigrations

# Apply migrations
python manage.py migrate

# Check migration status
python manage.py showmigrations
```

## 📞 Support & Contact

For issues, bugs, or feature requests, please contact the development team or submit an issue in the repository.

---

**Last Updated:** May 2026
