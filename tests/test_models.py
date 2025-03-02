from app.models.user import User
from app.models.generated_text import GeneratedText


def test_create_user(db):
    """Ensure a user can be created and retrieved."""
    user = User(username="testuser", password_hash="hashedpassword")
    db.add(user)
    db.commit()

    retrieved_user = db.query(User).filter_by(username="testuser").first()
    assert retrieved_user is not None
    assert retrieved_user.username == "testuser"


def test_create_generated_text(db):
    """Ensure generated text can be stored and retrieved."""
    user = User(username="testuser", password_hash="hashedpassword")
    db.add(user)
    db.commit()

    generated_text = GeneratedText(user_id=user.id, prompt="Tell me a joke", response="Here is a joke.")
    db.add(generated_text)
    db.commit()

    retrieved_text = db.query(GeneratedText).filter_by(user_id=user.id).first()
    assert retrieved_text is not None
    
    assert retrieved_text.prompt == "Tell me a joke"
    assert retrieved_text.response == "Here is a joke."