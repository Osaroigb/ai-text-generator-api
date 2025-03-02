import pytest
from app import app
from unittest.mock import patch
from app.database import db_session
from flask_jwt_extended import create_access_token
from app.models.generated_text import GeneratedText


@pytest.fixture
def client():
    """Create a test client with a clean database."""
    app.config["TESTING"] = True

    with app.test_client() as client:
        yield client

    db_session.rollback()


@pytest.fixture
def auth_header():
    """Generate a JWT token for authentication."""
    token = create_access_token(identity=1)  # Simulate a logged-in user
    return {"Authorization": f"Bearer {token}"}


@pytest.fixture
def create_text():
    """Helper function to create a generated text entry in the database."""
    def _create(user_id, prompt, response):
        text = GeneratedText(user_id=user_id, prompt=prompt, response=response)

        db_session.add(text)
        db_session.commit()

        return text
    
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
    assert "Text generated successfully." in response.json["message"]
    assert response.json["data"]["response"] == mock_response


def test_generate_text_invalid_prompt(client, auth_header):
    """Ensure invalid prompt input fails validation."""
    response = client.post(
        "/api/generate-text/",
        json={"prompt": "Hi"},
        headers=auth_header
    )

    assert response.status_code == 422
    assert "Invalid input." in response.json["error_message"]


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
    assert response.json["data"]["id"] == generated_text.id


def test_get_generated_text_not_found(client, auth_header):
    """Ensure retrieving a non-existent generated text fails."""
    response = client.get("/api/generate-text/99999", headers=auth_header)

    assert response.status_code == 404
    assert "Generated text not found." in response.json["error_message"]


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
    assert response.json["data"]["response"] == "Updated AI response."


def test_update_generated_text_unauthorized(client, create_text):
    """Ensure users cannot update someone else's generated text."""
    generated_text = create_text(user_id=2, prompt="Tell me a joke.", response="Old response.")  # Belongs to user 2

    response = client.put(
        f"/api/generate-text/{generated_text.id}",
        json={"response": "New AI response."},
        headers={"Authorization": "Bearer fake-token"}
    )

    assert response.status_code == 401  # Unauthorized


def test_delete_generated_text_success(client, auth_header, create_text):
    """Ensure deleting a generated text record succeeds."""
    generated_text = create_text(user_id=1, prompt="Tell me a joke.", response="Old response.")

    response = client.delete(f"/api/generate-text/{generated_text.id}", headers=auth_header)

    assert response.status_code == 200
    assert response.json["success"] is True
    assert "Generated text deleted successfully." in response.json["message"]


def test_delete_generated_text_not_found(client, auth_header):
    """Ensure deleting a non-existent generated text fails."""
    response = client.delete("/api/generate-text/99999", headers=auth_header)

    assert response.status_code == 404
    assert "Generated text not found." in response.json["error_message"]