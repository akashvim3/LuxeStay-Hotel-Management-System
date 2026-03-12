# LuxeStay - Hotel Management System

[![License: MIT](https://img.shields.io/badge/License-MIT-yellow.svg)](https://opensource.org/licenses/MIT)
[![Python 3.8+](https://img.shields.io/badge/python-3.8%2B-blue.svg)](https://www.python.org/downloads/)
[![Django 4.2](https://img.shields.io/badge/Django-4.2%2B-green.svg)](https://www.djangoproject.com/)

LuxeStay is a comprehensive, full-featured web application for managing hotel operations. It provides a seamless experience for both customers and administrators, covering everything from room bookings and restaurant reservations to event management and customer reviews.

## Table of Contents
- [Project Overview](#project-overview)
- [Features](#features)
- [Technologies Used](#technologies-used)
- [Prerequisites](#prerequisites)
- [Installation](#installation)
- [Running Tests](#running-tests)
- [Deployment](#deployment)
- [Project Structure](#project-structure)
- [Contributing](#contributing)
- [License](#license)
- [Contact](#contact)

## Project Overview
LuxeStay is built with Django and designed to handle all aspects of hotel management. The system includes modules for:
- User authentication and authorization
- Room inventory and booking management
- Restaurant operations (menu, table booking, inventory)
- Event management and ticketing
- Customer reviews and ratings
- Content management (blog, static pages)
- Gallery showcase
- RESTful API for extensibility

## Features
- **User Authentication:** Secure registration and login system for customers and staff with role-based access control.
- **Dashboard:** Separate dashboards for customers to view their bookings and for administrators to manage the entire property.
- **Room Management:** Advanced room management with seasonal pricing, availability tracking, and housekeeping status.
- **Booking System:** Easy-to-use booking process for rooms, including coupon and discount functionality, payment integration ready.
- **Restaurant Module:** Manage restaurant menus, handle table reservations, track inventory, and kitchen display system.
- **Event Management:** Create and manage hotel events, allowing users to book their spots with calendar integration.
- **Customer Reviews:** A dedicated system for users to leave and view reviews for their stays with moderation tools.
- **Blog & Pages:** A simple blogging engine and static pages (About, Contact) to engage with customers and improve SEO.
- **Gallery:** A responsive gallery to showcase the property rooms, facilities, and events.
- **REST API:** A basic API structure for potential mobile or third-party integrations (Django REST Framework ready).
- **Admin Panel:** Customized Django admin interface for efficient management of all entities.
- **Responsive Design:** Mobile-friendly interface using Bootstrap 5.
- **Internationalization:** Ready for multiple languages and currencies.

## Technologies Used
- **Backend:** Python 3.8+, Django 4.2+
- **Frontend:** HTML5, CSS3 (Bootstrap 5), JavaScript (Vanilla JS)
- **Database:** SQLite3 (development), configurable to PostgreSQL/MySQL for production
- **DevOps:** Docker, Docker Compose (for containerized deployment)
- **Other:**
  - Django Crispy Forms for beautiful forms
  - Pillow for image handling
  - Django Extensions for enhanced management commands
  - Gunicorn for production WSGI server
  - Whitenoise for static file serving in production

## Prerequisites
Before you begin, ensure you have met the following requirements:
- **Python** 3.8 or higher installed on your system
- **pip** (Python package installer) 
- **Git** (for cloning the repository)
- **Virtual environment** tool (venv or virtualenv)

## Installation
You can set up LuxeStay locally using either traditional method or Docker:

### Traditional Installation
1.  **Clone the repository:**
    ```bash
    git clone https://github.com/akashvim3/luxestay.git
    cd luxestay
    ```

2.  **Create a virtual environment:**
    ```bash
    # On Windows
    python -m venv venv
    venv\Scripts\activate
    
    # On macOS/Linux
    python -m venv venv
    source venv/bin/activate
    ```

3.  **Install dependencies:**
    ```bash
    pip install -r requirements.txt
    ```
    *Note: If requirements.txt doesn't exist, install Django and other dependencies:*
    ```bash
    pip install django pillow django-crispy-forms
    ```

4.  **Apply database migrations:**
    ```bash
    python manage.py migrate
    ```

5.  **Create a superuser to access the admin panel:**
    ```bash
    python manage.py createsuperuser
    ```
    Follow the prompts to create your admin account.

6.  **(Optional) Populate initial data:**
    If the `populate_data.py` script is configured, you can run it to add initial data to the database.
    ```bash
    python populate_data.py
    ```

### Docker Installation
1.  **Clone the repository:**
    ```bash
    git clone https://github.com/akashvim3/luxestay.git
    cd luxestay
    ```

2.  **Copy the example environment file and configure it:**
    ```bash
    cp .env.example .env
    # Edit .env to set your SECRET_KEY and other variables
    ```

3.  **Build and run with Docker Compose:**
    ```bash
    docker-compose up --build
    ```

4.  **Create a superuser (in another terminal):**
    ```bash
    docker-compose exec web python manage.py createsuperuser
    ```

## Running Tests
To ensure the application works correctly, run the test suite:

```bash
# Run all tests
python manage.py test

# Run tests for a specific app
python manage.py test accounts
python manage.py test bookings

# Run tests with coverage (if coverage.py is installed)
coverage run manage.py test
coverage report
```

## Deployment
For production deployment, consider the following steps:

### Traditional Deployment
1.  **Environment Configuration:**
    - Set `DEBUG = False` in `luxestay/settings.py`
    - Configure your `SECRET_KEY` and database settings
    - Set up allowed hosts

2.  **Static Files:**
    ```bash
    python manage.py collectstatic
    ```

3.  **Web Server:**
    - Use Gunicorn as the WSGI server:
      ```bash
      gunicorn luxestay.wsgi:application --bind 0.0.0.0:8000
      ```
    - Configure Nginx as a reverse proxy for serving static files and handling SSL

4.  **Database:**
    - Migrate to PostgreSQL or MySQL for better performance
    - Set up regular backups

5.  **Security:**
    - Implement HTTPS using SSL certificates
    - Set up CSRF protection and secure cookies
    - Consider using a service like Sentry for error tracking

### Docker Deployment (Recommended for Render)
You can deploy LuxeStay using Docker, which is ideal for platforms like Render:

1.  **Build and run with Docker Compose:**
    ```bash
    docker-compose up --build
    ```

2.  **For production on Render:**
    - Push your code to a GitHub repository
    - Connect your repository to Render
    - Create a new Web Service
    - Set the build command to: `docker build .`
    - Set the start command to: `gunicorn luxestay.wsgi:application --bind 0.0.0.0:$PORT`
    - Add environment variables as needed (SECRET_KEY, DEBUG, etc.)
    - Render will automatically detect your Dockerfile and docker-compose.yml

3.  **Manual Docker deployment:**
    ```bash
    # Build the image
    docker build -x luxestay .
    
    # Run the container
    docker run -p 8000:8000 --env-file .env luxestay
    ```

## Project Structure
```
luxestay/
├── accounts/           # User authentication and profiles
├── api/                # Django REST Framework API endpoints
├── blog/               # Blogging functionality
├── bookings/           # Room and table booking system
├── events/             # Event management
├── gallery/            # Image gallery
├── pages/              # Static pages (About, Contact, etc.)
├── restaurant/         # Restaurant management (menu, inventory, orders)
├── reviews/            # Customer review system
├── rooms/              # Room management and pricing
├── luxestay/           # Project settings and configuration
├── media/              # User-uploaded files (images, etc.)
├── static/             # CSS, JavaScript, and images
├── templates/          # HTML templates
├── manage.py           # Django command-line utility
├── populate_data.py    # Script to populate initial data
├── requirements.txt    # Python dependencies
├── Dockerfile          # Docker configuration for containerization
├── docker-compose.yml  # Docker Compose for multi-service deployment
└── .env.example        # Example environment variables
```

## Contributing
Contributions are welcome! If you have suggestions for improvements or want to report a bug, please feel free to open an issue or submit a pull request.

1. Fork the Project
2. Create your Feature Branch (`git checkout -b feature/AmazingFeature`)
3. Commit your Changes (`git commit -m 'Add some AmazingFeature'`)
4. Push to the Branch (`git push origin feature/AmazingFeature`)
5. Open a Pull Request

Please make sure to update tests as appropriate and follow the existing code style.

## License
This project is licensed under the MIT License. See the [LICENSE](LICENSE) file for more details.

## Contact
If you have any questions, feedback, or need support, please reach out:
- **Email:** support@luxestay.example.com
- **Issue Tracker:** [GitHub Issues](https://github.com/akashvim3/luxestay/issues)
- **Project Link:** [https://github.com/akashvim3/luxestay](https://github.com/akashvim3/)

---
*Developed with ❤️ for the hotel industry*
