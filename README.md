# join_backend

This is the backend API for a Kanban board application, built using Django and Django Rest Framework. The API provides endpoints to manage users, contacts, tasks and subtasks.

## Table of Contents

1. [Overview](#overview)
2. [Installation](#installation)
3. [Usage](#usage)
4. [API Documentation](#api-documentation)
5. [Testing](#testing)


## Overview

The API supports the following functionalities:
- **User Management**: Register, login, update, and delete user accounts.
- **Contact Management**: Create, update, delete, and list contacts.
- **Task Management**: Create tasks and subtasks, update their details, and delete them.

### Technologies Used

- **Django**: Web framework for building the backend.
- **Django Rest Framework**: Toolkit for building Web APIs.
- **SQLite**: Database used for data storage.

## Installation

### Prerequisites

Ensure you have the following installed:
- Python 3.11.4

### Setup

1. **Clone the repository:**

    ```bash
    git clone https://github.com/RicardoGeada/join-backend.git
    cd join-backend
    ```

2. **Create and activate a virtual environment:**

    ```bash
    python -m venv venv
    source venv/bin/activate  # On Windows: venv\Scripts\activate
    ```

3. **Install dependencies:**

    ```bash
    pip install -r requirements.txt
    ```

4. **Set up the database:**

    SQLite is configured by default, so you can simply apply the migrations:

    ```bash
    python manage.py migrate
    ```

5. **Create a superuser:**

    ```bash
    python manage.py createsuperuser
    ```

6. **Run the development server:**

    ```bash
    python manage.py runserver
    ```


## Usage

After starting the server, the API will be available at `http://127.0.0.1:8000/`. You can interact with the API using tools like `curl`, Postman, or directly through the browser for GET requests.


## API Documentation

### Endpoints Overview

- **User Management**
  - `POST /api/register/` - Register a new user
  - `POST /api/login/` - Login a user
  - `GET /api/users/` - Retrieve users details
  - `GET /api/users/{id}/` - Retrieve user details
  - `PUT /api/users/{id}/` - Update user details
  - `DELETE /api/users/{id}/` - Delete a user account

- **Contact Management**
  - `GET /api/contacts/` - List all contacts
  - `POST /api/contacts/` - Create a new contact
  - `GET /api/contacts/{id}/` - Retrieve a specific contact
  - `PUT /api/contacts/{id}/` - Update a contact
  - `DELETE /api/contacts/{id}/` - Delete a contact

- **Task Management**
  - `GET /api/tasks/` - List all tasks
  - `POST /api/tasks/` - Create a new task
  - `GET /api/tasks/{id}/` - Retrieve a specific task
  - `PUT /api/tasks/{id}/` - Update a task
  - `DELETE /api/tasks/{id}/` - Delete a task

- **Subtask Management**
  - `GET /api/subtasks/` - List all subtasks for a task
  - `POST /api/subtasks/` - Create a new subtask
  - `GET /api/subtasks/{id}/` - Retrieve a specific subtask
  - `PUT /api/subtasks/{id}/` - Update a subtask
  - `DELETE /api/subtasks/{id}/` - Delete a subtask


## Testing

To run the test suite:

```bash
python manage.py test