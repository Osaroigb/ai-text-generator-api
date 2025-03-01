import jwt
from app.config import Config
from app.utils.errors import UnauthorizedError
from datetime import datetime, timedelta, timezone


class JWTHandler:
    """Handles JWT token creation, validation, and decoding."""

    @staticmethod
    def generate_token(user_id: int) -> str:
        """
        Generate a JWT token for a user.
        :param user_id: The ID of the user.
        :return: Encoded JWT token as a string.
        """    
        payload = {
            "identity": user_id,
            "exp": datetime.now(timezone.utc) + timedelta(seconds=Config.JWT_EXPIRY_IN_SECONDS)
        }

        token = jwt.encode(payload, Config.JWT_SECRET_KEY, algorithms="HS256")
        return token


    @staticmethod
    def decode_jwt(token: str) -> dict:
        """
        Decode a JWT token and validate its authenticity.
        :param token: JWT token string.
        :return: Decoded payload.
        :raises UnauthorizedError: If token is invalid or expired.
        """
        try:
            decoded_token = jwt.decode(
                token, 
                Config.JWT_SECRET_KEY, 
                algorithms="HS256",
                options={"require_exp": True}
            )

            return decoded_token
        
        except jwt.ExpiredSignatureError:
            raise UnauthorizedError("Token has expired.")
        
        except jwt.InvalidTokenError:
            raise UnauthorizedError("Invalid authentication token.")
        

    @staticmethod
    def get_user_id(token: str) -> int:
        """
        Extract user ID from a JWT token.
        
        :param token: The token that was sent to the server.
        :return: The user ID from the token payload.
        :raises UnauthorizedError: If token is invalid or expired.
        """
        try:
            data = jwt.decode(
                token,
                Config.JWT_SECRET_KEY,
                algorithms=["HS256"],
                options={"require_exp": True},
            )
            
            return data["identity"]

        except jwt.ExpiredSignatureError:
            raise UnauthorizedError("Token has expired.")

        except jwt.InvalidTokenError:
            raise UnauthorizedError("Invalid authentication token.")