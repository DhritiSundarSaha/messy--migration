

import os
import tempfile
import pytest
import json
from app import create_app
from app.db import init_db

@pytest.fixture
def app():
    """Create and configure a new app instance for each test."""
    # Create a temporary file to act as the database
    db_fd, db_path = tempfile.mkstemp()

    app = create_app()
    app.config.update({
        "TESTING": True,
        "DATABASE": db_path,
    })

    # Initialize the temporary database with the schema
    with app.app_context():
        init_db()

    yield app

    os.close(db_fd)
    os.unlink(db_path)

@pytest.fixture
def client(app):
    """A test client for the app."""
    return app.test_client()


def test_home(client):
    """Test the health check endpoint."""
    rv = client.get('/')
    assert rv.status_code == 200
    assert b"User Management System is running" in rv.data

def test_create_and_login_user(client):
    """Test creating a new user and then logging in."""
    # Create a user
    new_user = {
        "name": "Test User",
        "email": "test@example.com",
        "password": "a-secure-password"
    }
    rv = client.post('/users', data=json.dumps(new_user), content_type='application/json')
    assert rv.status_code == 201
    response_data = json.loads(rv.data)
    assert response_data['status'] == 'success'

    # Login
    login_details = {"email": "test@example.com", "password": "a-secure-password"}
    rv = client.post('/login', data=json.dumps(login_details), content_type='application/json')
    assert rv.status_code == 200
    assert json.loads(rv.data)['status'] == 'success'

    bad_login_details = {"email": "test@example.com", "password": "wrong-password"}
    rv = client.post('/login', data=json.dumps(bad_login_details), content_type='application/json')
    assert rv.status_code == 401
    assert json.loads(rv.data)['status'] == 'error'

def test_get_nonexistent_user(client):
    """Test that fetching a user who doesn't exist returns a 404."""
    rv = client.get('/user/99999')
    assert rv.status_code == 404
    assert b"not found" in rv.data