# School Management API

A Django REST Framework API for a school management system with role-based access control for Principals, Teachers, and Students. This project is designed to be a comprehensive learning resource for understanding Django, DRF, and JWT authentication.

## Features

- **Role-Based Access Control:** Differentiates between `Principal`, `Teacher`, and `Student` roles.
- **JWT Authentication:** Secure authentication using JSON Web Tokens (Access and Refresh tokens).
- **Customized Token Response:** Includes user details (`id`, `email`, `role`) in the login response.
- **Comprehensive Data Models:**
    - `User`: Custom user model with roles.
    - `Student`: Linked to a user, can enroll in multiple classes.
    - `Teacher`: Linked to a user, can teach multiple classes and be a class teacher for one.
    - `Class`: Represents a classroom, can have multiple subjects.
    - `Subject`: Represents a subject taught in a class.
- **Database Seeder:** A management command to populate the database with initial test data.

## Getting Started

### Prerequisites

- Python 3.10+
- Pip (Python package installer)
- Git

### Installation

1.  **Clone the repository:**
    ```bash
    git clone <your-repository-url>
    cd school-management-drf-api
    ```

2.  **Create and activate a virtual environment:**
    ```bash
    # For Linux/macOS
    python3 -m venv .venv
    source .venv/bin/activate

    # For Windows
    python -m venv .venv
    .venv\Scripts\activate
    ```

3.  **Install dependencies:**
    ```bash
    pip install -r requirements.txt
    ```

4.  **Run database migrations:**
    ```bash
    python manage.py makemigrations
    python manage.py migrate
    ```

5.  **Seed the database with initial data:**
    ```bash
    python manage.py seed_school
    ```

6.  **Run the development server:**
    ```bash
    python manage.py runserver
    ```
    The API will be available at `http://127.0.0.1:8000/`.

## API Endpoints and Usage

### Authentication

#### `POST /api/auth/login/`

Authenticates a user and returns an access token, refresh token, and user details.

**Request Body:**

```json
{
    "email": "student1@example.com",
    "password": "password123"
}
```

**Success Response (200 OK):**

```json
{
    "refresh": "eyJhbGciOiJIUzI1NiIsInR5cCI6IkpXVCJ9...",
    "access": "eyJhbGciOiJIUzI1NiIsInR5cCI6IkpXVCJ9...",
    "user": {
        "id": 1,
        "email": "student1@example.com",
        "role": "student"
    }
}
```

#### `POST /api/token/refresh/`

Refreshes an expired access token using a valid refresh token.

**Request Body:**

```json
{
    "refresh": "your-refresh-token"
}
```

**Success Response (200 OK):**

```json
{
    "access": "new-access-token"
}
```

---

## Deep Dive: Core Concepts

### 1. Django and Django REST Framework (DRF)

-   **Django:** A high-level Python web framework that enables rapid development of secure and maintainable websites. It follows the **Model-View-Template (MVT)** architectural pattern.
    -   **Model:** The data layer. Defines the structure of your data (database tables).
    -   **View:** The business logic layer. Handles requests and returns responses.
    -   **Template:** The presentation layer. Renders the data for the user (in our case, DRF handles rendering to JSON).
-   **Django REST Framework (DRF):** A powerful and flexible toolkit built on top of Django for building Web APIs. It simplifies the process of creating RESTful services.

### 2. Project Structure

-   `config/`: Project-level configuration (`settings.py`, `urls.py`).
-   `accounts/`: A Django "app" for user authentication and management.
-   `school/`: A Django "app" for the core school-related models and logic.
-   `manage.py`: A command-line utility for interacting with your Django project.

### 3. Models and Relationships

File: `school/models.py`

-   **`OneToOneField`:** Creates a one-to-one relationship. In our `Student` and `Teacher` models, each user can only be one student or one teacher.
-   **`ManyToManyField`:** Creates a many-to-many relationship.
    -   A `Student` can be in multiple `Class`es.
    -   A `Class` can have multiple `Subject`s.
    -   A `Teacher` can teach multiple `Class`es.
-   **`ForeignKey`:** Creates a many-to-one relationship. A `Teacher` can be the `class_teacher_of` one `Class`.

### 4. JWT Authentication

-   **What is JWT?** JSON Web Tokens are a compact, URL-safe means of representing claims to be transferred between two parties. They are used for stateless authentication.
-   **How it works:**
    1.  A user logs in with their credentials.
    2.  The server verifies the credentials and, if correct, generates an **access token** and a **refresh token**.
    3.  The server sends these tokens back to the client.
    4.  The client stores these tokens and sends the **access token** in the `Authorization` header of every subsequent request to a protected endpoint.
    5.  The server decodes the JWT and, if valid, processes the request.
-   **Access Token vs. Refresh Token:**
    -   **Access Token:** Short-lived. Used to access protected resources.
    -   **Refresh Token:** Long-lived. Used to obtain a new access token when the old one expires, without requiring the user to log in again.

### 5. Serializers

File: `accounts/serializers.py`

-   **What are they?** Serializers convert complex data types (like Django model instances) into native Python datatypes that can be easily rendered into JSON. They also handle deserialization and data validation.
-   **`UserSerializer`:** Converts `User` model instances into JSON, showing only the `id`, `email`, and `role`.
-   **`CustomTokenSerializer`:**
    -   It inherits from `TokenObtainPairSerializer` from the `simple-jwt` library.
    -   We override the `validate` method to add our custom user data to the token response. This is how we get the `user` object in the login response.

### 6. Views

File: `accounts/views.py`

-   **What are they?** Views handle the logic for processing requests and returning responses.
-   **`CustomLoginView`:**
    -   This is a class-based view that inherits from `TokenObtainPairView`.
    -   By setting `serializer_class = CustomTokenSerializer`, we tell this view to use our custom serializer, which in turn gives us the custom login response.

### 7. URLs

File: `config/urls.py`

-   This file maps URL patterns to views.
-   We've added the paths for `TokenObtainPairView` and `TokenRefreshView` from `simple-jwt` to handle token creation and refreshing.
-   We've also included the URLs from our `accounts` app under the `/api/auth/` path.

This `README.md` provides a solid foundation. As we build out more features (like creating, reading, updating, and deleting students, teachers, etc.), we can add more endpoints and explanations to this guide.

---

## How Authentication Works: From "Numb" to "Aha!"

If you're coming from traditional Django, the way DRF and JWT handle authentication can feel like magic. Let's break it down.

**The Core Difference: Stateful vs. Stateless**

-   **Traditional Django (Stateful):** Uses **sessions**. After you log in, the server creates a session in its database and gives your browser a `sessionid` cookie. On every request, the browser sends the cookie, and the server looks up the session to identify you. The server "remembers" you.

-   **DRF with JWT (Stateless):** The server does **not** remember you. After you log in, it gives you a **JSON Web Token (JWT)**. This token is a self-contained, digitally signed package of information that proves who you are. The server doesn't need to store anything.


### Step-by-Step Breakdown

#### Step 1: The Login (Getting the Token)

1.  **You send:** A `POST` request to `/api/auth/login/` with your `email` and `password`.
2.  **The Server does:**
    -   The `TokenObtainPairView` uses Django's standard `authenticate()` function to check your credentials against the database. **This is the same database check traditional Django does.**
    -   If valid, it generates a signed **access token** and **refresh token**. The signature, created with your project's `SECRET_KEY`, is crucial—it proves the token is authentic and hasn't been tampered with.
    -   Our `CustomTokenSerializer` adds your `user` details to the response.
3.  **You get:** A JSON response with your tokens and user info. The server immediately "forgets" you.

#### Step 2: Accessing a Protected Page (Using the Token)

1.  **You send:** A request to a protected endpoint (e.g., `GET /api/students/`). You must include an `Authorization` header:
    `Authorization: Bearer <your_access_token>`
2.  **The Server does (The "Magic"):**
    -   The `JWTAuthentication` class (which we set as the default) automatically inspects the request for this header.
    -   **Verification:** It checks the token's signature and expiration date. If either is invalid, it rejects the request with a `401 Unauthorized` error.
    -   **Hydration:** If the token is valid, it decodes the payload to get the user's ID. It then does a quick database lookup (`User.objects.get(id=...)`) to get the full user object.
    -   It attaches this user object to the `request` object. Now, inside your view, `request.user` is available, just like in traditional Django!
3.  **You get:** The data you requested, because the server now trusts who you are for the duration of this single request.

### Summary: The Key Takeaway

The database check isn't gone, it has just moved.

-   **Traditional Django:** Checks the database on **every request** using a session ID.
-   **DRF with JWT:**
    1.  Checks the database **once at login** to issue the token.
    2.  On subsequent requests, it **cryptographically verifies the token first**. If the token is valid, *then* it does a quick database lookup to get the full user object.

This stateless approach is what makes APIs fast, scalable, and flexible.
