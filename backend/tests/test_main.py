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


def test_articles_are_ordered_newest_first(client, author_with_articles):
    response = client.get("/api/articles")

    assert response.status_code == 200
    titles = [article["title"] for article in response.json()]
    assert titles == ["Newer Article", "Older Article"]


def test_articles_respect_limit(client, author_with_articles):
    response = client.get("/api/articles?limit=1")

    assert response.status_code == 200
    titles = [article["title"] for article in response.json()]
    assert titles == ["Newer Article"]


def test_list_author_articles_returns_404_when_author_does_not_exist(client):
    response = client.get("/api/users/23/articles")

    assert response.status_code == 404
    assert response.json() == {"detail": "Author not found"}


def test_empty_articles_for_author(client, author_without_articles):
    response = client.get(f"/api/users/{author_without_articles}/articles")

    assert response.status_code == 200
    assert response.json() == []
