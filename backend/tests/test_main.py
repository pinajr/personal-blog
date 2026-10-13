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
