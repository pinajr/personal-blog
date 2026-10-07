import os

from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker, declarative_base

DATABASE_URL = os.environ["DATABASE_URL"]

engine = create_engine(DATABASE_URL)
SessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)
Base = declarative_base()


def get_session():
    # Yields a session scoped to a single request; FastAPI resumes this
    # generator after the request finishes, running db.close() via the
    # finally block regardless of whether the request succeeded or failed.
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()
