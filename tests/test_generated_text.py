import pytest
from app import app
from unittest.mock import patch
from app.models.user import User
from flask_jwt_extended import create_access_token
from app.models.generated_text import GeneratedText


@pytest.fixture
def client():
    """Create a test client with a clean database."""
    app.config["TESTING"] = True

    with app.test_client() as client:
        yield client


@pytest.fixture
def auth_header():
    """Generate a JWT token for authentication within the app context."""
    with app.app_context():
        token = create_access_token(identity=1)  # Simulate a logged-in user

    return {"Authorization": f"Bearer {token}"}


@pytest.fixture
def create_text(db_session):
    """Create and return a generated text entry."""
    def _create(user_id, prompt, response):
        # Ensure the user exists before inserting generated text
        user = db_session.query(User).filter_by(id=user_id).first()

        if not user:
            user = User(id=user_id, username=f"user{user_id}", password_hash="hashedpassword")
            db_session.add(user)
            db_session.commit()
        
        generated_text = GeneratedText(user_id=user_id, prompt=prompt, response=response)

        db_session.add(generated_text)
        db_session.commit()

        return generated_text
    
    return _create


# 🔹 **UNIT TESTS** - Validate input handling & responses

def test_generate_text_success(client, auth_header):
    """Ensure text generation succeeds and stores response."""
    mock_response = "This is a generated AI response."

    with patch("app.services.openai_service.OpenAIService.generate_text", return_value=mock_response):
        response = client.post(
            "/api/generate-text/",
            json={"prompt": "Tell me a joke."},
            headers=auth_header
        )

    assert response.status_code == 201
    assert response.json["success"] is True
    assert response.json["message"] == "Text generated successfully."
    assert "data" in response.json


def test_generate_text_invalid_prompt(client, auth_header):
    """Ensure invalid prompt input fails validation."""
    response = client.post(
        "/api/generate-text/",
        json={"prompt": "Hi"},
        headers=auth_header
    )

    assert response.status_code == 422
    assert "Invalid input." in response.json["message"]


def test_generate_text_unauthorized(client):
    """Ensure request fails if no authentication token is provided."""
    response = client.post(
        "/api/generate-text/",
        json={"prompt": "Tell me a joke."}
    )

    assert response.status_code == 401  # Unauthorized


# 🔹 **INTEGRATION TESTS** - Full lifecycle testing

def test_get_generated_text_success(client, auth_header, create_text):
    """Ensure a generated text record can be retrieved."""
    generated_text = create_text(user_id=1, prompt="Tell me a joke.", response="Here's a joke.")

    response = client.get(f"/api/generate-text/{generated_text.id}", headers=auth_header)

    assert response.status_code == 200
    assert response.json["success"] is True
    assert response.json["message"] == "Generated text retrieved successfully."
    assert "data" in response.json


def test_get_generated_text_not_found(client, auth_header):
    """Ensure retrieving a non-existent generated text fails."""
    response = client.get("/api/generate-text/99999", headers=auth_header)

    assert response.status_code == 404
    assert response.json["message"] == "Generated text not found."


def test_update_generated_text_success(client, auth_header, create_text):
    """Ensure updating a generated text record succeeds."""
    generated_text = create_text(user_id=1, prompt="Tell me a joke.", response="Old response.")

    response = client.put(
        f"/api/generate-text/{generated_text.id}",
        json={"response": "Updated AI response."},
        headers=auth_header
    )

    assert response.status_code == 200
    assert response.json["success"] is True
    assert response.json["message"] == "Generated text updated successfully."


def test_update_generated_text_unauthorized(client, create_text):
    """Ensure users cannot update someone else's generated text."""
    generated_text = create_text(user_id=2, prompt="Tell me a joke.", response="Old response.")  # Belongs to user 2

    response = client.put(
        f"/api/generate-text/{generated_text.id}",
        json={"response": "New AI response."},
        headers={"Authorization": "Bearer fake-token"}
    )

    assert response.status_code == 401  # Unauthorized
    assert response.json["message"] == "Unauthorized access."


def test_delete_generated_text_success(client, auth_header, create_text):
    """Ensure deleting a generated text record succeeds."""
    generated_text = create_text(user_id=1, prompt="Tell me a joke.", response="Old response.")

    response = client.delete(f"/api/generate-text/{generated_text.id}", headers=auth_header)

    assert response.status_code == 200
    assert response.json["success"] is True
    assert response.json["message"] == "Generated text deleted successfully."


def test_delete_generated_text_not_found(client, auth_header):
    """Ensure deleting a non-existent generated text fails."""
    response = client.delete("/api/generate-text/99999", headers=auth_header)

    assert response.status_code == 404
    assert response.json["message"] == "Generated text not found."