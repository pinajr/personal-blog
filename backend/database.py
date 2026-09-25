from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker, declarative_base

# Hardcoded for local development without a password. Will move to an
# environment variable before this touches production (Phase 8).
DATABASE_URL = "postgresql://localhost/personal_blog"

engine = create_engine(DATABASE_URL)
SessionLocal = sessionmaker(bind=engine)
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