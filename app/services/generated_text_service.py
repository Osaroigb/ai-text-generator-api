from app.database import db_session
from app.models.generated_text import GeneratedText
from app.utils.errors import NotFoundError, UnauthorizedError

class GeneratedTextService:
    """Service for handling generated text storage and retrieval."""

    @staticmethod
    def store_generated_text(user_id: int, prompt: str, response: str) -> dict:
        """
        Store generated text in the database.
        """
        new_text = GeneratedText(user_id=user_id, prompt=prompt, response=response)
        
        db_session.add(new_text)
        db_session.commit()

        return {
            "id": new_text.id,
            "user_id": user_id,
            "prompt": prompt,
            "response": response,
            "timestamp": new_text.timestamp
        }


    @staticmethod
    def get_text_by_id(text_id: int, user_id: int) -> dict:
        """
        Retrieve a generated text by ID.
        """
        text = db_session.query(GeneratedText).filter_by(id=text_id).first()

        if not text:
            raise NotFoundError("Generated text not found.")
        
        if text.user_id != user_id:
            raise UnauthorizedError("You are not authorized to access this resource.")
        
        return {
            "id": text.id,
            "user_id": text.user_id,
            "prompt": text.prompt,
            "response": text.response,
            "timestamp": text.timestamp
        }


    @staticmethod
    def update_text(text_id: int, user_id: int, new_response: str) -> dict:
        """
        Update the response of a generated text.
        """
        text = db_session.query(GeneratedText).filter_by(id=text_id).first()

        if not text:
            raise NotFoundError("Generated text not found.")
        
        if text.user_id != user_id:
            raise UnauthorizedError("You are not authorized to update this resource.")
        
        text.response = new_response
        db_session.commit()

        return {
            "id": text.id,
            "user_id": text.user_id,
            "prompt": text.prompt,
            "response": text.response,
            "timestamp": text.timestamp
        }


    @staticmethod
    def delete_text(text_id: int, user_id: int):
        """
        Delete a stored generated text.
        """
        text = db_session.query(GeneratedText).filter_by(id=text_id).first()

        if not text:
            raise NotFoundError("Generated text not found.")
        
        if text.user_id != user_id:
            raise UnauthorizedError("You are not authorized to delete this resource.")
        
        db_session.delete(text)
        db_session.commit()