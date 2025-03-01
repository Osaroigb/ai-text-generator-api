from app.config import Config
from app.models.user import Base
from sqlalchemy import create_engine
from sqlalchemy.orm import scoped_session, sessionmaker

engine = create_engine(Config.DATABASE_URL, pool_size=10, max_overflow=20)
db_session = scoped_session(sessionmaker(autocommit=False, autoflush=False, bind=engine))

def init_db():
    """Initialize database tables."""

    from app.models import user 
    Base.metadata.create_all(bind=engine)

