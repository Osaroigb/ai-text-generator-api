from app.database import Base
from sqlalchemy.orm import relationship
from sqlalchemy import Column, Integer, Text, ForeignKey, DateTime, func

class GeneratedText(Base):
    """Model for storing AI-generated responses."""
    
    __tablename__ = "generated_texts"

    id = Column(Integer, primary_key=True, autoincrement=True)
    user_id = Column(Integer, ForeignKey("users.id"), nullable=False, index=True)
    prompt = Column(Text, nullable=False)
    response = Column(Text, nullable=False)
    timestamp = Column(DateTime, default=func.now(), nullable=False)

    # Define relationship with the User model
    user = relationship("User", back_populates="generated_text")