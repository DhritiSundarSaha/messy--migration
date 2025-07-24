
from flask import request, jsonify, Blueprint, Response, abort
from werkzeug.security import check_password_hash, generate_password_hash
from .db import get_db

bp = Blueprint('api', __name__)

@bp.route('/')
def home() -> Response:
    """Provides a basic health check for the API."""
    return jsonify({"status": "success", "message": "User Management System is running."})

@bp.route('/users', methods=['GET'])
def get_all_users() -> Response:
    """Retrieves a list of all users."""
    db = get_db()
    # In a further abstraction, this SQL would be in a dedicated function in `db.py`
    users = db.execute("SELECT id, name, email FROM users").fetchall()
    return jsonify([dict(user) for user in users])

@bp.route('/user/<int:user_id>', methods=['GET'])
def get_user(user_id: int) -> Response:
    """Retrieves a single user by their ID."""
    db = get_db()
    # This logic would ideally be in a db.get_user_by_id(user_id) function.
    user = db.execute("SELECT id, name, email FROM users WHERE id = ?", (user_id,)).fetchone()
    
    if user is None:
        # Triggers the 404 error handler registered in app/__init__.py
        abort(404, description="User not found")
    
    return jsonify(dict(user))

@bp.route('/users', methods=['POST'])
def create_user() -> Response:
    """Creates a new user."""
    data = request.get_json()
    if not data or not all(k in data for k in ('name', 'email', 'password')):
        abort(400, description="Missing name, email, or password")

    name = data['name']
    email = data['email']
    password = generate_password_hash(data['password'])
    
    db = get_db()
    try:
        # This logic would ideally be in a db.create_user(...) function.
        cursor = db.execute(
            "INSERT INTO users (name, email, password) VALUES (?, ?, ?)",
            (name, email, password)
        )
        db.commit()
    except db.IntegrityError:
        # Triggers a 409 Conflict error handler.
        abort(409, description=f"User with email {email} already exists.")

    return jsonify({"status": "success", "message": "User created", "user_id": cursor.lastrowid}), 201

@bp.route('/user/<int:user_id>', methods=['PUT'])
def update_user(user_id: int) -> Response:
    """Updates a user's name or email."""
    data = request.get_json()
    if not data or not any(k in data for k in ('name', 'email')):
        abort(400, description="Invalid data; requires 'name' or 'email' field")

    # This logic would ideally be in a db.update_user(...) function.
    name = data.get('name')
    email = data.get('email')
    
    db = get_db()
    updates, params = [], []
    if name:
        updates.append("name = ?")
        params.append(name)
    if email:
        updates.append("email = ?")
        params.append(email)
    
    params.append(user_id)
    
    db.execute(f"UPDATE users SET {', '.join(updates)} WHERE id = ?", tuple(params))
    db.commit()
    
    return jsonify({"status": "success", "message": f"User {user_id} updated"})

@bp.route('/user/<int:user_id>', methods=['DELETE'])
def delete_user(user_id: int) -> Response:
    """Deletes a user."""
    db = get_db()
    # This logic would ideally be in a db.delete_user(user_id) function.
    db.execute("DELETE FROM users WHERE id = ?", (user_id,))
    db.commit()
    
    # 204 No Content is the standard for a successful deletion with no body.
    return Response(status=204)

@bp.route('/search', methods=['GET'])
def search_users() -> Response:
    """Searches for users by name."""
    name = request.args.get('name')
    if not name:
        abort(400, description="Please provide a 'name' query parameter.")
    
    db = get_db()
    # This logic would ideally be in a db.search_users_by_name(name) function.
    users = db.execute("SELECT id, name, email FROM users WHERE name LIKE ?", ('%' + name + '%',)).fetchall()
    return jsonify([dict(user) for user in users])

@bp.route('/login', methods=['POST'])
def login() -> Response:
    """Handles user login."""
    data = request.get_json()
    if not data or not all(k in data for k in ('email', 'password')):
        abort(400, description="Missing email or password")

    email = data['email']
    password = data['password']
    
    db = get_db()
    # This logic would ideally be in a db.get_user_by_email(email) function.
    user = db.execute("SELECT * FROM users WHERE email = ?", (email,)).fetchone()
    
    if user and check_password_hash(user['password'], password):
        return jsonify({"status": "success", "user_id": user['id']})
    
    abort(401, description="Invalid credentials")