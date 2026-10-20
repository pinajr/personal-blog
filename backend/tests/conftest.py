import os

# Keep tests independent from the developer's PostgreSQL database.
os.environ["DATABASE_URL"] = "sqlite://"

import pytest
from datetime import datetime, timezone, timedelta
from fastapi.testclient import TestClient
from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker
from sqlalchemy.pool import StaticPool

from models import Article, User, LoginSession
from database import Base, get_session
from main import app
from security import get_password_hash, generate_session_token, digest_session_token


@pytest.fixture
def db_session():
    test_engine = create_engine(
        "sqlite://",
        connect_args={"check_same_thread": False},
        poolclass=StaticPool,
    )
    Base.metadata.create_all(bind=test_engine)

    testing_session_local = sessionmaker(
        autocommit=False,
        autoflush=False,
        bind=test_engine,
    )

    db = testing_session_local()
    try:
        yield db
    finally:
        db.close()
        Base.metadata.drop_all(bind=test_engine)
        test_engine.dispose()


@pytest.fixture
def client(db_session):
    def override_get_session():
        return db_session

    app.dependency_overrides[get_session] = override_get_session

    try:
        with TestClient(app) as test_client:
            yield test_client
    finally:
        app.dependency_overrides.pop(get_session, None)


@pytest.fixture
def author_with_articles(db_session):
    author = User(
        username="test-author",
        email="author@example.com",
        password_hash="test-hash",
    )
    db_session.add(author)
    db_session.commit()

    older_article = Article(
        title="Older Article",
        content="Older content.",
        created_at=datetime(2026, 1, 1),
        author_id=author.id,
    )
    newer_article = Article(
        title="Newer Article",
        content="Newer content",
        created_at=datetime(2026, 1, 2),
        author_id=author.id,
    )
    db_session.add_all([older_article, newer_article])
    db_session.commit()

    return author


@pytest.fixture
def author_without_articles(db_session):
    author = User(
        username="test-author",
        email="author@example.com",
        password_hash="test-hash",
    )
    db_session.add(author)
    db_session.commit()

    return author


@pytest.fixture
def article(db_session):
    author = User(
        username="test-author",
        email="author@example.com",
        password_hash="test-hash",
    )
    db_session.add(author)
    db_session.commit()

    new_article = Article(
        title="New Article",
        content="New content.",
        created_at=datetime(2026, 1, 1),
        author_id=author.id,
    )
    db_session.add(new_article)
    db_session.commit()

    return new_article


@pytest.fixture
def user_with_password(db_session):
    password_hash = get_password_hash('test-password')
    user = User(
        username="test-user",
        email="user@example.com",
        password_hash=password_hash,
    )
    db_session.add(user)
    db_session.commit()

    return user


@pytest.fixture
def article_owned_by_user(db_session, user_with_password):
    article = Article(
        title="Test Article",
        content="Test content.",
        created_at=datetime(2026, 1, 1),
        author_id=user_with_password.id,
    )
    db_session.add(article)
    db_session.commit()

    return article


@pytest.fixture
def expired_session_token(db_session, user_with_password):
    token = generate_session_token()
    login = LoginSession(
        token_hash=digest_session_token(token),
        user_id=user_with_password.id,
        expires_at=datetime.now(timezone.utc) - timedelta(minutes=1),
    )
    db_session.add(login)
    db_session.commit()

    return token
