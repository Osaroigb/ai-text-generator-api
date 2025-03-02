from sqlalchemy import create_engine
from app.config import Config, logging
from sqlalchemy.orm import declarative_base
from sqlalchemy.orm import scoped_session, sessionmaker

engine = create_engine(Config.DATABASE_URL, echo=False, pool_size=10, max_overflow=20)
db_session = scoped_session(sessionmaker(autocommit=False, autoflush=False, bind=engine))

Base = declarative_base()

def init_db():
    """Initialize database tables."""

    from app.models import user, generated_text
    Base.metadata.create_all(bind=engine)
    
    logging.info("Database connected successfully!")