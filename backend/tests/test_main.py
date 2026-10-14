from datetime import datetime

from models import User, Article


def test_health(client):
    response = client.get("/api/health")
    assert response.status_code == 200
    assert response.json() == {"status": "ok"}


def test_articles_reject_limit_below_minimum(client):
    response = client.get("/api/articles?limit=0")
    assert response.status_code == 422


def test_articles_reject_limit_above_maximum(client):
    response = client.get("/api/articles?limit=101")
    assert response.status_code == 422


def test_list_articles_returns_empty_list(client):
    response = client.get("/api/articles")
    assert response.status_code == 200
    assert response.json() == []


def test_articles_are_ordered_newest_first(client, db_session):
    author = User(
        username="test-author",
        email="author@example.com",
        password_hash="test-hash",
    )
    db_session.add(author)
    db_session.commit()
    db_session.refresh(author)

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

    response = client.get("/api/articles")

    assert response.status_code == 200
    titles = [article["title"] for article in response.json()]
    assert titles == ["Newer Article", "Older Article"]
