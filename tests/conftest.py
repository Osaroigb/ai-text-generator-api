import pytest
from app import app
from app.database import engine
from app.models.user import User
from sqlalchemy.orm import sessionmaker
from app.models.generated_text import GeneratedText


@pytest.fixture(scope="session")
def test_app():
    """Create a test client for the Flask app."""
    app.config["TESTING"] = True

    with app.test_client() as client:
        yield client


@pytest.fixture(scope="session")
def db():
    """Set up a test database and return the session."""
    # Create a new test database in memory
    Session = sessionmaker(bind=engine)
    session = Session()

    # Create tables
    User.metadata.create_all(engine)
    GeneratedText.metadata.create_all(engine)

    yield session  # Provide the session to the tests

    # Teardown: Drop tables after test session
    session.close()
    User.metadata.drop_all(engine)
    GeneratedText.metadata.drop_all(engine)


@pytest.fixture(scope="function", autouse=True)
def clean_db(db):
    """Clean up the database after each test function."""
    db.query(GeneratedText).delete()
    db.query(User).delete()
    db.commit()
    
    yield
    db.rollback()  # Rollback any changes made during a test