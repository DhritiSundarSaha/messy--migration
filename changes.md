# Refactoring Changes for Messy Migration

This document outlines the major issues identified in the legacy codebase and the changes implemented to address them.

## 1. Major Issues Identified

The initial codebase, while functional, suffered from critical flaws that made it unsuitable for a production environment.

* **Critical Security Vulnerabilities**:
    * **SQL Injection**: All database queries were constructed using f-strings, directly embedding user input into SQL commands. This is a top-tier vulnerability.
    * **Plaintext Passwords**: Passwords were stored and checked in plaintext, meaning a database breach would expose all user credentials.

* **Poor Code Organization**:
    * **Single-File Architecture**: All application logic, routing, and database management were contained in a single `app.py` file, violating the principle of separation of concerns.
    * **Global State**: The database connection was managed as a global variable, which is not a safe or scalable pattern for web applications.

* **Lack of Best Practices**:
    * **Inconsistent API Responses**: Endpoints returned data in non-standard formats (e.g., `str(list_of_tuples)`) instead of conventional JSON.
    * **No Proper HTTP Status Codes**: Most endpoints returned `200 OK` regardless of the outcome (e.g., resource creation or client errors).
    * **No Input Validation**: The API blindly trusted incoming data, leading to potential errors and security risks.
    * **No Error Handling**: Database or parsing errors were not handled gracefully.

## 2. Changes Made and Justification

### a. Security Improvements (Highest Priority)

* **Parameterized SQL Queries**: **Every single SQL query was rewritten** to use parameterized statements (`?`). This is the standard, secure way to pass data to a database, completely eliminating the risk of SQL injection.
* **Password Hashing**: We now use `werkzeug.security` to hash passwords (`generate_password_hash`) before storing them and to safely compare them during login (`check_password_hash`). This ensures that even if the database is compromised, user passwords remain secure.
* **Disabled Debug Mode**: The default runner (`app.py`) no longer enables debug mode by default, preventing the exposure of the interactive debugger in a production scenario.

### b. Code Organization and Structure

* **Application Factory Pattern**: The project was restructured to use a standard application factory (`create_app`). This makes the application more modular, easier to test, and scalable.
* **Blueprints for Routing**: Routes were moved into `app/routes.py` and organized under a Flask Blueprint. This cleanly separates routing logic from the main application setup.
* **Per-Request Database Connections**: Database logic was moved to `app/db.py`. The `get_db()` function ensures a new connection is opened for each request and closed automatically afterward, which is the standard and most reliable method.
* **Centralized Configuration**: A `config.py` file was introduced to store configuration variables, separating them from the application code.

### c. Implementation of Best Practices

* **Standardized JSON Responses**: All API endpoints now return well-formed JSON objects with a consistent structure (e.g., `{"status": "success", "data": ...}`).
* **Correct HTTP Status Codes**: Each endpoint now returns the semantically correct HTTP status code:
    * `201 Created` for successful resource creation.
    * `204 No Content` for successful deletion.
    * `400 Bad Request` for invalid or missing client data.
    * `401 Unauthorized` for failed logins.
    * `404 Not Found` for requests targeting non-existent resources.
    * `409 Conflict` for attempting to create a user with an email that already exists.
* **Input Validation**: Added checks in `create_user` and `login` to ensure required fields are present in the request body.
* **Robust Error Handling**: Added `try...except` blocks for database operations that could fail (like inserting a user with a duplicate email).

### d. Testing

* **Test Suite Added**: A new `tests/` directory was created with a `test_api.py` file. We added tests for critical functionality like user creation, login (both success and failure cases), and handling of "not found" errors. This provides a safety net against future regressions.

## 3. Assumptions and Trade-offs

* **Simplicity over Complexity**: To meet the time constraints, I chose a simple file-based structure over more complex patterns like a full-blown Object-Relational Mapper (ORM) like SQLAlchemy. An ORM would further improve maintainability but would be an over-engineering for this specific assignment.
* **Basic Validation**: Input validation is present but minimal (checking for key existence). A production system would benefit from more robust validation (e.g., email format, password complexity rules).

## 4. What I Would Do With More Time

* **Introduce an ORM**: Integrate SQLAlchemy to replace raw SQL queries. This would make database interactions more Pythonic, abstract away database-specific syntax, and make schema migrations easier.
* **Schema Validation**: Implement a data validation library like Marshmallow or Pydantic to define schemas for request/response data, providing automatic validation and serialization.
* **Authentication & Authorization**: The current login endpoint is basic. I would implement a token-based authentication system (e.g., JWT) to secure endpoints, requiring users to send a token with subsequent requests.
* **Containerization**: Dockerize the application for consistent development and deployment environments.
* **CI/CD Pipeline**: Set up a basic continuous integration pipeline (e.g., using GitHub Actions) to automatically run tests on every push.