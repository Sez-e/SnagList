from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker
from .database import SQLALCHEMY_DATABASE_URL  # noqa

engine = create_engine(SQLALCHEMY_DATABASE_URL)

SessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)

def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()
