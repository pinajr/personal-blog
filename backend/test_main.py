from fastapi.testclient import TestClient

from main import app

client = TestClient(app)


def test_health():
    response = client.get("/api/health")
    assert response.status_code == 200
    assert response.json() == {"status": "ok"}


def test_articles_reject_limit_below_minimum():
    response = client.get("/api/articles?limit=0")
    assert response.status_code == 422


def test_articles_reject_limit_above_maximum():
    response = client.get("/api/articles?limit=101")
    assert response.status_code == 422
