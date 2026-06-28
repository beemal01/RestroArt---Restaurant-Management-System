# RestroArt - Restaurant Management System

A full-featured **Restaurant Management Web Application** built with **Django 6**, **Django REST Framework**, **PostgreSQL**, **Redis**, and **Celery**. RestroArt handles everything from browsing a dynamic menu and managing a shopping cart to placing orders and booking tables - all wrapped in a polished, responsive frontend with automated email confirmations.

---

## Features

### Menu and Browsing

- **Dynamic Menu Display** - Browse food items with images, prices, ratings, descriptions, and chef tags.
- **Search and Filter** - Search by title, category, or chef tags with server-side filtering.
- **Responsive Pagination** - Paginated API responses (9 items per page) with customizable limits.
- **Smart Caching** - Menu list is cached for 2 hours and automatically invalidated when food items are added, updated, or deleted.

### Cart and Checkout

- **Persistent Cart** - Authenticated users can add, update quantity, or remove items.
- **Auto-Merge Quantities** - Adding the same item twice increases the quantity instead of creating duplicates.
- **Rate-Limited Checkout** - Throttled to 2 checkouts per hour per user.
- **Email Confirmation** - On checkout, an HTML email with item breakdown, 13% tax calculation, and grand total is sent via Celery.

### Table Reservation

- **Flexible Booking** - Reserve tables for various party sizes (1 to 10+ people).
- **Time Slots** - Choose from multiple time slots across lunch and dinner hours.
- **Rate-Limited** - Maximum 2 reservations per day per user.
- **Email Confirmation** - A beautifully formatted HTML email confirms the booking details.

### Authentication

- **JWT-Based Auth** - Secure access and refresh token flow using `djangorestframework-simplejwt`.
- **Custom User Model** - Extended Django `AbstractUser` with name, email, and phone number.
- **Token Blacklisting** - Logout invalidates refresh tokens for security.
- **Email and Password Login** - Users authenticate via email and password.

### Background Tasks (Celery)

- **Async Email Sending** - Order confirmations and reservation emails are dispatched in the background so the UI never blocks.
- **Redis as Broker** - Celery uses Redis for task queuing and result storage.
- **Windows-Compatible Pool** - Configured to use the `solo` pool on Windows to avoid multiprocessing issues.

### Security and Performance

- **Throttling** - Anonymous users limited to 10 requests/minute; checkout and reservation endpoints have their own scoped limits.
- **Caching** - Redis-backed caching for frequently accessed menu data.
- **Token Blacklisting** - Revoked tokens can't be reused.
- **Environment Variables** - All sensitive credentials loaded from `.env`.

---

## Tech Stack

| Layer            | Technology                                    |
|------------------|-----------------------------------------------|
| **Framework**    | Django 6.0.6                                  |
| **API**          | Django REST Framework 3.17.1                  |
| **Auth**         | SimpleJWT (Access + Refresh token, Blacklist) |
| **Database**     | PostgreSQL                                    |
| **Cache/Queue**  | Redis                                         |
| **Task Queue**   | Celery 5.6.3                                  |
| **Frontend**     | HTML, CSS, Bootstrap 5, JavaScript, Swiper.js |
| **Email**        | SMTP (Gmail) with HTML templates              |
| **Icons**        | Font Awesome 6 (Pro)                          |

---

## Project Structure

```text
RestroArt/
├── Restro/                  # Django project settings
│   ├── settings.py          # Main configuration (DB, cache, auth, throttling)
│   ├── urls.py              # Root URL configuration
│   ├── wsgi.py
│   └── asgi.py
│
├── authApp/                 # Authentication app
│   ├── models.py            # Custom User model
│   ├── serializers.py       # Register, Login, Logout serializers
│   ├── views.py             # Signup, Signin, Logout API + page views
│   └── urls.py              # Auth routes
│
├── restroApp/               # Core restaurant app
│   ├── models.py            # Food, Cart, Reservation models
│   ├── serializers.py       # Food, Cart, Reservation serializers
│   ├── views.py             # All API endpoints + page views
│   ├── urls.py              # App routes
│   ├── tasks.py             # Celery async tasks (email sending)
│   ├── celery.py            # Celery app configuration
│   ├── signals.py           # Cache invalidation on Food changes
│   ├── pagination.py        # Custom pagination (9 items/page)
│   └── admin.py             # Admin panel registration
│
├── templates/               # HTML templates
│   ├── base.html            # Base layout
│   ├── index.html           # Homepage
│   ├── menu.html            # Menu page
│   ├── cart.html            # Shopping cart
│   ├── reservation.html     # Reservation form
│   ├── contact.html         # Contact page
│   ├── signup.html          # Signup page
│   ├── signin.html          # Signin page
│   └── emails/              # Email templates
│       ├── order_confirmation.html
│       └── reservation_confirmation.html
│
├── static/                  # Static assets
│   ├── css/                 # Bootstrap, custom styles, AOS, Swiper
│   ├── js/                  # jQuery, Bootstrap, custom scripts
│   ├── img/                 # Images (menu, chefs, portfolio, etc.)
│   └── webfonts/            # Font Awesome icons
│
├── media/                   # Uploaded menu images
├── manage.py                # Django management script
├── requirements.txt         # Python dependencies
├── Dockerfile               # Docker image for Django + Celery
├── compose.yml              # Docker Compose (PostgreSQL, Redis, Django, Celery)
├── .env                     # Environment variables (DB, email, Docker config)
└── .gitignore
```

---

## Getting Started

### Prerequisites

- **Option A (Manual):** Python 3.13+, PostgreSQL, Redis
- **Option B (Recommended):** [Docker Desktop](https://www.docker.com/products/docker-desktop/) (handles PostgreSQL, Redis, and the app in containers)
- A Gmail account for sending emails (or any SMTP provider)

---

## Docker Setup (Quick Start) 🐳

Run the entire application — Django, PostgreSQL, Redis, and Celery — with a single command.

### 1. Clone and Enter the Project

```bash
git clone <repository-url>
cd RestroArt
```

### 2. Configure Environment

The included `.env` file already contains sensible defaults for Docker. Verify or adjust:

```env
# Database Configuration
DB_NAME=restro_db
DB_USER=your_db_user
DB_PASSWORD=your_db_password

# Docker-specific Database Variables (used by compose.yml)
POSTGRES_DB=restro_db
POSTGRES_USER=your_db_user
POSTGRES_PASSWORD=your_db_password

# Docker Connection Strings (uses service names)
DATABASE_URL=postgres://${POSTGRES_USER}:${POSTGRES_PASSWORD}@db:5432/${POSTGRES_DB}
CELERY_BROKER_URL=redis://redis:6379/0
CELERY_RESULT_BACKEND=redis://redis:6379/0

# Email Configuration (Gmail example)
EMAIL_HOST_USER=your_email@gmail.com
EMAIL_HOST_PASSWORD=your_app_password
```

> **Note:** Inside Docker containers, services communicate via their service names (`db`, `redis`). The `DATABASE_URL` and `CELERY_BROKER_URL` already reference these automatically.

### 3. Build and Start All Services

```bash
docker compose up --build
```

This starts four containers:

| Container       | Service        | Purpose                               |
|-----------------|----------------|-------------------------------------  |
| `restroApp`     | Django Web     | Serves the app at `localhost:8000`    |
| `celery_worker` | Celery Worker  | Processes background email tasks      |
| `db`            | PostgreSQL 17  | Database server on port `5432`        |
| `redis`         | Redis 7        | Cache & message broker on port `6379` |

### 4. Run Migrations

In a **new terminal**, run:

```bash
docker compose exec django_web python manage.py migrate
```

### 5. Create a Superuser

```bash
docker compose exec django_web python manage.py createsuperuser
```

### 6. Access the Application

Open [http://localhost:8000](http://localhost:8000) in your browser.

---

### Useful Docker Commands

```bash
# View logs
docker compose logs -f

# Stop all containers
docker compose down

# Stop and remove volumes (reset database)
docker compose down -v

# Run management commands
docker compose exec django_web python manage.py <command>

# Rebuild after dependency changes
docker compose up --build
```

---

## Manual Setup (Without Docker)

### 1. Clone and Setup

```bash
git clone <repository-url>
cd RestroArt
```

### 2. Create Virtual Environment

```bash
python -m venv venv
venv\Scripts\activate      # Windows
source venv/bin/activate   # macOS/Linux
```

### 3. Install Dependencies

```bash
pip install -r requirements.txt
```

### 4. Configure Environment Variables

Create a `.env` file in the project root (a template is already included):

```env
# Database Configuration
DB_NAME=restro_db
DB_USER=db_username
DB_PASSWORD=db-passowrd

# Email Configuration (Gmail example)
EMAIL_HOST_USER=your_email@gmail.com
EMAIL_HOST_PASSWORD=your_app_password
```

> **Note:** For Gmail, you will need an App Password (not your regular password).

### 5. Create the Database

Open PostgreSQL and create the database:

```sql
CREATE DATABASE restro_db;
CREATE USER your_db_user WITH PASSWORD 'your_db_password';
ALTER ROLE your_db_user SET client_encoding TO 'utf8';
ALTER ROLE your_db_user SET default_transaction_isolation TO 'read committed';
ALTER ROLE your_db_user SET timezone TO 'UTC';
GRANT ALL PRIVILEGES ON DATABASE restro_db TO your_db_user;
```

### 6. Run Migrations

```bash
python manage.py makemigrations
python manage.py migrate
```

### 7. Create a Superuser

```bash
python manage.py createsuperuser
```

### 8. Start Redis

Make sure Redis is running on `localhost:6379`. On Windows you can use WSL:

```bash
# WSL
sudo apt install redis-server
sudo service redis-server start
```

On macOS/Linux:

```bash
redis-server
```

> **Tip:** If you prefer Docker, skip the manual steps above and use the **[Docker Setup](#docker-setup-quick-start-)**, which runs everything automatically.

### 9. Start Celery Worker

Open a **new terminal** (with the virtual environment activated):

```bash
# Windows
celery -A restroApp worker --pool=solo -l info

# macOS/Linux
celery -A restroApp worker -l info
```

### 10. Run the Development Server

```bash
python manage.py runserver
```

Visit [http://127.0.0.1:8000](http://127.0.0.1:8000) to see the application.

---

## API Endpoints

### Authentication (authApp)

| Method | Endpoint                  | Description            | Auth Required |
|--------|---------------------------|------------------------|---------------|
| GET    | `/signup/`                | Signup page            | No            |
| GET    | `/signin/`                | Signin page            | No            |
| POST   | `/api/signupview/`        | Register a new user    | No            |
| POST   | `/api/signinview/`        | Login, get JWT tokens  | No            |
| POST   | `/api/logoutview/`        | Logout, blacklist token| Yes           |

### Restaurant (restroApp)

| Method | Endpoint                       | Description                   | Auth Required |
|--------|--------------------------------|-------------------------------|---------------|
| GET    | `/`                            | Homepage                      | No            |
| GET    | `/menu/`                       | Menu page                     | No            |
| GET    | `/reservation/`                | Reservation page              | No            |
| GET    | `/contact/`                    | Contact page                  | No            |
| GET    | `/api/homeview/`               | Top 6 food items              | No            |
| GET    | `/api/foodlist/`               | Paginated food list (search)  | No            |
| POST   | `/api/foodview/`               | Add new food item             | Yes (Admin)   |
| GET    | `/api/cartview/`               | List cart items               | Yes           |
| POST   | `/api/cartview/`               | Add item to cart              | Yes           |
| GET    | `/api/cartview/<id>/`          | Get specific cart item        | Yes           |
| PUT    | `/api/cartview/<id>/`          | Update cart item quantity     | Yes           |
| DELETE | `/api/cartview/<id>/`          | Remove cart item              | Yes           |
| POST   | `/api/checkout/`               | Place order, clear cart       | Yes           |
| POST   | `/api/reservationview/`        | Book a table                  | Yes           |

### Query Parameters

Food List example - `/api/foodlist/?search=pizza&page=2&limit=12`:

- `search` - Filter by title, category, or chef tags
- `page` - Page number (default: 1)
- `limit` - Items per page (default: 9)

---

## Email Templates

RestroArt sends two types of HTML emails:

1. **Order Confirmation** - Includes item list, quantities, subtotal, 13% tax, and grand total.
2. **Reservation Confirmation** - Includes guest name, date, time, and party size.

All emails are rendered from Django templates in `templates/emails/` and sent asynchronously via Celery.

---

## Configuration Highlights

### Throttling Rates (settings.py)

```python
'DEFAULT_THROTTLE_RATES': {
    'anon': '10/minute',        # Anonymous users
    'checkout': '2/hour',       # Checkout endpoint
    'reservation': '2/day',     # Reservation endpoint
}
```

### JWT Configuration

```python
SIMPLE_JWT = {
    "ACCESS_TOKEN_LIFETIME": timedelta(days=1),
    "REFRESH_TOKEN_LIFETIME": timedelta(days=1),
}
```

### Caching (Redis)

- **Backend:** `django_redis.cache.RedisCache`
- **Location:** `redis://127.0.0.1:6379/1`
- **Food List Cache:** 2 hours - auto-invalidated on any Food model save/delete via signals.

---

## Running Tests

```bash
python manage.py test
```

---

## Contributing

Contributions are welcome! Here is how you can help:

1. Fork the repository.
2. Create a feature branch: `git checkout -b awesome-feature`
3. Commit your changes: `git commit -m 'Add awesome feature'`
4. Push to the branch: `git push origin awesome-feature`
5. Open a Pull Request.

Please make sure your code follows Django best practices and includes appropriate tests.

---

## License

This project is open source and available under the [MIT License](LICENSE).

---

## Acknowledgements

- [Django](https://www.djangoproject.com/) and [Django REST Framework](https://www.django-rest-framework.org/)
- [Celery](https://docs.celeryq.dev/) - Async task queue
- [Redis](https://redis.io/) - In-memory data store
- [Bootstrap 5](https://getbootstrap.com/) - Frontend framework
- [Font Awesome](https://fontawesome.com/) - Icons
- [Swiper.js](https://swiperjs.com/) - Touch slider

---

*Made with love for restaurants and food lovers.*
