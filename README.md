# Puddle — Online Marketplace

A full-stack marketplace web application built with Django, where users can discover products, publish listings, and communicate with sellers.

## Overview

Puddle is a web application designed to provide a simple marketplace experience. Users can browse available products, search listings, explore categories, publish their own items, and contact sellers through an integrated messaging system.

This project was built to develop practical skills in backend development, database management, authentication, and responsive web interfaces.

## Features

* **User Authentication** — User registration, login, and logout.
* **Product Listings** — Create and publish product listings with descriptions, prices, and images.
* **Product Search** — Search products by name and description.
* **Category Filtering** — Browse products by category.
* **Product Details** — View product information and related items.
* **Seller Dashboard** — Manage personal listings.
* **Messaging System** — Conversations between buyers and sellers.
* **Image Storage** — Cloudinary integration for product images.
* **Database Integration** — SQLite for local development and PostgreSQL support for deployment.
* **Responsive UI** — Interface styled with Tailwind CSS.

## Tech Stack

| Technology          | Purpose                           |
| ------------------- | --------------------------------- |
| Python              | Programming language              |
| Django              | Backend web framework             |
| Django ORM          | Database operations               |
| SQLite / PostgreSQL | Data persistence                  |
| HTML                | Page structure                    |
| Tailwind CSS        | Styling and responsive design     |
| Cloudinary          | Image storage                     |
| WhiteNoise          | Static file serving configuration |
| Git & GitHub        | Version control                   |

## Project Structure

```text
puddle/
├── puddle/          # Project configuration and root URLs
├── core/            # Main pages, contact page and shared functionality
├── dashboard/       # User dashboard
├── item/            # Product listings, categories and search
├── conversation/    # Buyer-seller messaging
├── manage.py
├── requirements.txt
└── README.md
```

## Getting Started

### Prerequisites

* Python 3.11+
* Git
* A Cloudinary account for image uploads
* PostgreSQL connection string if using PostgreSQL instead of SQLite

### 1. Clone the repository

```bash
git clone https://github.com/adamelaouane/puddle.git
cd puddle
```

### 2. Create a virtual environment

**Windows PowerShell:**

```powershell
py -3.11 -m venv env
.\env\Scripts\Activate.ps1
```

### 3. Install dependencies

```bash
python -m pip install -r requirements.txt
```

### 4. Configure environment variables

Set your configuration in PowerShell. Use your own Cloudinary credentials and keep secrets private.

```powershell
$env:DEBUG = "True"
$env:DJANGO_SECRET_KEY = "your-local-development-secret"
$env:CLOUDINARY_CLOUD_NAME = "your-cloud-name"
$env:CLOUDINARY_API_KEY = "your-api-key"
$env:CLOUDINARY_API_SECRET = "your-api-secret"
```

To use PostgreSQL, also configure `DATABASE_URL` with your own connection string. If it is not set, the project configuration falls back to SQLite.

Never commit API secrets, database credentials, or production secret keys to GitHub.

### 5. Apply database migrations

```bash
python manage.py migrate
```

### 6. Create an administrator account

```bash
python manage.py createsuperuser
```

### 7. Run the development server

```bash
python manage.py runserver
```

Open http://127.0.0.1:8000/ in your browser.

## Configuration Notes

* Environment variables must be configured again when opening a new PowerShell session.
* PostgreSQL is intended for persistent hosted data.
* Cloudinary credentials are required for image uploads when using the configured Cloudinary storage backend.
* Production deployment requires appropriate secret-key, host, database, and static-file settings.

## Future Improvements

* Add automated tests for core features.
* Improve product filtering and sorting.
* Add pagination for product listings.
* Enhance form validation and error handling.
* Complete production deployment and document the live application.

## Author

**Adam Elaouane**

Computer Science Student | Aspiring Full-Stack Developer

GitHub: [@adamelaouane](https://github.com/adamelaouane)

---

*Built as a hands-on project to practice Django development, database integration, authentication, and full-stack web application design.*
