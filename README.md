# Django Task Management API

A RESTful API for managing projects and tasks, built with Django. Features authentication, CRUD operations, and relational data modeling.

## Features

- **User Authentication**: Session-based login/logout.
- **Project Management**: Create, read, update, and delete projects.
- **Task Management**: Bulk create, update, and delete tasks within projects.
- **RESTful Design**: Follows REST conventions with JSON responses.
- **Error Handling**: Detailed validation and error messages.

## Tech Stack

- **Backend**: Django 4.2+
- **Database**: SQLite (default), PostgreSQL-ready
- **Authentication**: Session-based (Django `contrib.auth`)
- **API Design**: Pure Django (no DRF)

## Installation

1. **Clone the repository**:
   ```bash
   git clone https://github.com/wajahathassan-dev/django_restapi_session_based_auth.git
   cd django_restapi_session_based_auth
   ```

2. **Set up a virtual environment**:
    ```bash
    python -m venv venv
    source venv/bin/activate  # Linux/Mac
    venv\Scripts\activate    # Windows
    ```

3. **Install dependencies**:
    ```bash
    pip install -r requirements.txt
    ```

4. **Generate migrations**:
    ```bash
    python manage.py makemigrations
    ```

5. **Apply migrations**:
    ```bash
    python manage.py migrate
    ```

6. **Start the server**:
    ```bash
    python manage.py runserver
    ```
