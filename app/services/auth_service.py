from app.models.user import User
from app.database import db_session
from app.utils.jwt_handler import JWTHandler
from app.utils.errors import UnauthorizedError, UnprocessableEntityError
from werkzeug.security import generate_password_hash, check_password_hash

class AuthService:
    """Handles user authentication: registration and login."""

    @staticmethod
    def register_user(username: str, password: str) -> dict:
        """
        Register a new user.
        :param username: User's unique username.
        :param password: Raw password to hash.
        :return: User ID and username.
        :raises UnprocessableEntityError: If username is already taken.
        """

        existing_user = db_session.query(User).filter_by(username=username).first()

        if existing_user:
            raise UnprocessableEntityError("Username is already in use.")

        hashed_password = generate_password_hash(password)
        new_user = User(username=username, password_hash=hashed_password)

        db_session.add(new_user)
        db_session.commit()

        return { "user_id": new_user.id, "username": new_user.username }


    @staticmethod
    def authenticate_user(username: str, password: str) -> str:
        """
        Authenticate user credentials and return a JWT token.
        :param username: User's username.
        :param password: User's raw password.
        :return: user ID & JWT token.
        :raises UnauthorizedError: If authentication fails.
        """

        user = db_session.query(User).filter_by(username=username).first()

        if not user:
            raise UnauthorizedError("Invalid username.")
        
        if not check_password_hash(user.password_hash, password):
            raise UnauthorizedError("Incorrect password.")

        token = JWTHandler.generate_token(user.id)
        return { "user_id": user.id, "access_token": token }