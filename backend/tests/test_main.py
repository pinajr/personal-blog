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


def test_list_author_articles_returns_empty_list(client, author_without_articles):
    response = client.get(f"/api/users/{author_without_articles.id}/articles")

    assert response.status_code == 200
    assert response.json() == []


def test_list_author_articles_returns_articles(client, author_with_articles):
    response = client.get(f"/api/users/{author_with_articles.id}/articles")

    assert response.status_code == 200
    titles = [article["title"] for article in response.json()]
    assert titles == ["Newer Article", "Older Article"]


def test_list_author_articles_respects_limit(client, author_with_articles):
    response = client.get(
        f"/api/users/{author_with_articles.id}/articles?limit=1"
    )

    assert response.status_code == 200
    titles = [article["title"] for article in response.json()]
    assert titles == ["Newer Article"]


def test_author_articles_reject_limit_below_minimum(client):
    response = client.get("/api/users/23/articles?limit=0")

    assert response.status_code == 422


def test_author_articles_reject_limit_above_maximum(client):
    response = client.get("/api/users/23/articles?limit=101")

    assert response.status_code == 422


def test_get_article_returns_404_when_article_does_not_exist(client):
    response = client.get("/api/articles/999")

    assert response.status_code == 404
    assert response.json() == {"detail": "Article not found"}


def test_get_article_returns_article_when_it_exists(client, article):
    response = client.get(f"/api/articles/{article.id}")

    assert response.status_code == 200

    article_data = response.json()
    assert article_data["title"] == "New Article"
    assert article_data["content"] == "New content."


def test_create_article_requires_authentication(client):
    response = client.post(
        "/api/articles",
        json={
            "title": "Test Article",
            "content": "Test content.",
        },
    )

    assert response.status_code == 401
    assert response.json() == {"detail": "Invalid or expired session"}


def test_login_sets_session_cookie(client, user_with_password):
    response = client.post(
        "/api/login",
        json={
            "username": user_with_password.username,
            "password": 'test-password',
        },
    )

    assert response.status_code == 200
    assert response.json() == {"message": "Logged in successfully"}
    assert response.cookies.get("session_token") is not None


def test_create_article_with_authenticated_user(client, user_with_password):
    response = client.post(
        "/api/login",
        json={
            "username": user_with_password.username,
            "password": 'test-password',
        },
    )
    assert response.status_code == 200

    response = client.post(
        "/api/articles",
        json={
            "title": "Test Article",
            "content": "Test content.",
        },
    )
    assert response.status_code == 201

    article_data = response.json()
    assert article_data["title"] == "Test Article"
    assert article_data["content"] == "Test content."
    assert article_data["author_id"] == user_with_password.id


def test_login_rejects_incorrect_password(client, user_with_password):
    response = client.post(
        "/api/login",
        json={
            "username": user_with_password.username,
            "password": "wrong-password",
        },
    )

    assert response.status_code == 401
    assert response.json() == {"detail": "Invalid credentials"}


def test_login_rejects_unknown_username(client, user_with_password):
    response = client.post(
        "/api/login",
        json={
            "username": "wrong-username",
            "password": "test-password",
        },
    )

    assert response.status_code == 401
    assert response.json() == {"detail": "Invalid credentials"}


def test_logout_succeeds_without_session(client):
    response = client.post("/api/logout")

    assert response.status_code == 200
    assert response.json() == {"message": "Logged out successfully"}


def test_logout_invalidates_session(client, user_with_password):
    response = client.post(
        "/api/login",
        json={
            "username": user_with_password.username,
            "password": "test-password",
        },
    )
    assert response.status_code == 200
    token = response.cookies.get("session_token")
    assert token is not None

    response = client.post("/api/logout")
    assert response.status_code == 200

    client.cookies.set("session_token", token)
    response = client.post(
        "/api/articles",
        json={
            "title": "Test Article",
            "content": "Test content.",
        },
    )

    assert response.status_code == 401
    assert response.json() == {"detail": "Invalid or expired session"}


def test_update_article_requires_authentication(client):
    response = client.put(
        "/api/articles/1",
        json={
            "title": "Test Article",
            "content": "Test content.",
        },
    )

    assert response.status_code == 401
    assert response.json() == {"detail": "Invalid or expired session"}


def test_delete_article_requires_authentication(client):
    response = client.delete("/api/articles/1")

    assert response.status_code == 401
    assert response.json() == {"detail": "Invalid or expired session"}


def test_update_article_forbidden_for_non_owner(client, user_with_password, article):
    response = client.post(
        "/api/login",
        json={
            "username": user_with_password.username,
            "password": "test-password",
        },
    )
    assert response.status_code == 200

    response = client.put(
        f"/api/articles/{article.id}",
        json={
            "title": "Test Article",
            "content": "Test content.",
        },
    )

    assert response.status_code == 403
    assert response.json() == {"detail": "You don't own this article"}


def test_delete_article_forbidden_for_non_owner(client, user_with_password, article):
    response = client.post(
        "/api/login",
        json={
            "username": user_with_password.username,
            "password": "test-password",
        },
    )
    assert response.status_code == 200

    response = client.delete(f"/api/articles/{article.id}")

    assert response.status_code == 403
    assert response.json() == {"detail": "You don't own this article"}


def test_owner_can_update_article(client, user_with_password, article_owned_by_user):
    response = client.post(
        "/api/login",
        json={
            "username": user_with_password.username,
            "password": "test-password",
        },
    )
    assert response.status_code == 200

    response = client.put(
        f"/api/articles/{article_owned_by_user.id}",
        json={
            "title": "A New Title",
            "content": "A new content.",
        },
    )
    assert response.status_code == 200

    article_data = response.json()
    assert article_data["title"] == "A New Title"
    assert article_data["content"] == "A new content."


def test_owner_can_delete_article(client, user_with_password, article_owned_by_user):
    response = client.post(
        "/api/login",
        json={
            "username": user_with_password.username,
            "password": "test-password",
        },
    )
    assert response.status_code == 200

    response = client.delete(f"/api/articles/{article_owned_by_user.id}")
    assert response.status_code == 200
    assert response.json() == {"message": "Article deleted successfully"}

    response = client.get(f"/api/articles/{article_owned_by_user.id}")
    assert response.status_code == 404
