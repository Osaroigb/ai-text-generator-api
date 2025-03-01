from app.database import Base
from sqlalchemy import Column, Integer, String

class User(Base):
    """User model for authentication."""
    
    __tablename__ = "users"

    id = Column(Integer, primary_key=True, autoincrement=True)
    username = Column(String, unique=True, nullable=False)
    password_hash = Column(String, nullable=False)