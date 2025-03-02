import pytest
from app import app
from app.models.user import User
from app.database import db_session

@pytest.fixture
def client():
    """Create a test client with a clean database."""
    app.config["TESTING"] = True

    with app.test_client() as client:
        yield client

    # Cleanup database after each test
    db_session.rollback()


@pytest.fixture
def create_user():
    """Helper function to create a user in the database."""
    def _create(username, password_hash):
        user = User(username=username, password_hash=password_hash)
        db_session.add(user)
        db_session.commit()
        return user
    return _create


def test_register_invalid_username(client):
    """Ensure that a short username fails validation."""
    response = client.post("/api/auth/register", json={"username": "ab", "password": "securepassword"})
    assert response.status_code == 422
    assert "Invalid input." in response.json["error_message"]


def test_register_invalid_password(client):
    """Ensure that a short password fails validation."""
    response = client.post("/api/auth/register", json={"username": "validUser", "password": "123"})
    assert response.status_code == 422
    assert "Invalid input." in response.json["error_message"]


def test_register_success(client):
    """Ensure a user can successfully register."""
    response = client.post("/api/auth/register", json={"username": "testuser", "password": "securepassword"})
    assert response.status_code == 201
    assert response.json["success"] is True
    assert "User registered successfully" in response.json["message"]
    assert "username" in response.json["data"]


def test_register_duplicate_username(client):
    """Ensure duplicate usernames cannot be registered."""
    client.post("/api/auth/register", json={"username": "testuser", "password": "securepassword"})
    response = client.post("/api/auth/register", json={"username": "testuser", "password": "newpassword"})
    
    assert response.status_code == 422
    assert "Username is already in use." in response.json["error_message"]


def test_login_invalid_username(client):
    """Ensure that logging in with an invalid username fails."""
    response = client.post("/api/auth/login", json={"username": "ab", "password": "securepassword"})
    assert response.status_code == 422
    assert "Invalid input." in response.json["error_message"]


def test_login_invalid_password(client):
    """Ensure that logging in with an invalid password fails."""
    response = client.post("/api/auth/login", json={"username": "validUser", "password": "123"})
    assert response.status_code == 422
    assert "Invalid input." in response.json["error_message"]


def test_login_non_existent_user(client):
    """Ensure logging in with a non-existent user fails."""
    response = client.post("/api/auth/login", json={"username": "nouser", "password": "securepassword"})
    assert response.status_code == 401
    assert "Invalid username or password." in response.json["error_message"]


def test_login_success(client):
    """Ensure a user can successfully log in."""
    client.post("/api/auth/register", json={"username": "testuser", "password": "securepassword"})
    response = client.post("/api/auth/login", json={"username": "testuser", "password": "securepassword"})

    assert response.status_code == 200
    assert response.json["success"] is True
    assert "Login successful" in response.json["message"]
    assert "token" in response.json["data"]


def test_login_wrong_password(client):
    """Ensure login fails with incorrect password."""
    client.post("/api/auth/register", json={"username": "testuser", "password": "securepassword"})
    response = client.post("/api/auth/login", json={"username": "testuser", "password": "wrongpassword"})

    assert response.status_code == 401
    assert "Invalid username or password." in response.json["error_message"]