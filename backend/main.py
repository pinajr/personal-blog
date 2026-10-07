from datetime import datetime, timedelta, timezone

from typing import Annotated
from fastapi import Cookie, Depends, FastAPI, HTTPException, Response, Query
from sqlalchemy.orm import Session

from auth import get_current_user
from database import get_session
from models import Article, LoginSession, User
from security import (
    digest_session_token,
    generate_session_token,
    verify_password,
)
from schemas import (
    ArticleCreate,
    ArticleResponse,
    ArticleUpdate,
    LoginRequest,
    UserResponse,
)

SESSION_LIFETIME = timedelta(minutes=30)
app = FastAPI()


@app.get("/api/health")
def health_check():
    return {"status": "ok"}


@app.post("/api/login")
def login(
    credentials: LoginRequest,
    response: Response,
    db: Session = Depends(get_session),
):
    user = db.query(User).filter(User.username == credentials.username).first()
    if user is None or not verify_password(credentials.password, user.password_hash):
        raise HTTPException(status_code=401, detail="Invalid credentials")

    token = generate_session_token()
    new_session = LoginSession(
        token_hash=digest_session_token(token),
        user_id=user.id,
        expires_at=datetime.now(timezone.utc) + SESSION_LIFETIME,
    )
    db.add(new_session)
    db.commit()

    response.set_cookie(
        key="session_token", value=token, httponly=True,
        max_age=int(SESSION_LIFETIME.total_seconds()),
        secure=False,
        samesite="lax",
        path="/",
    )
    return {"message": "Logged in successfully"}


@app.post("/api/logout")
def logout(
    response: Response,
    session_token: str | None = Cookie(default=None),
    db: Session = Depends(get_session),
):
    message = {"message": "Logged out successfully"}
    response.delete_cookie(key="session_token", path="/")

    if session_token is None:
        return message
    token_hash = digest_session_token(session_token)

    login_session = (
        db.query(LoginSession)
        .filter(LoginSession.token_hash == token_hash)
        .first()
    )
    if login_session is None:
        return message

    db.delete(login_session)
    db.commit()
    return message


@app.get("/api/users/{user_id}", response_model=UserResponse)
def get_user(user_id: int, db: Session = Depends(get_session)):
    user = db.query(User).filter(User.id == user_id).first()
    if user is None:
        raise HTTPException(status_code=404, detail="User not found")
    return user
    

@app.get("/api/users/{user_id}/articles", response_model=list[ArticleResponse])
def list_author_articles(
    user_id: int,
    limit: Annotated[int, Query(ge=1, le=100)] = 5,
    db: Session = Depends(get_session),
):
    author = db.query(User).filter(User.id == user_id).first()
    if author is None:
        raise HTTPException(status_code=404, detail="Author not found")
    return (
        db.query(Article)
        .filter(Article.author_id == user_id)
        .order_by(Article.created_at.desc(), Article.id.desc())
        .limit(limit)
        .all()
    )


@app.get("/api/articles", response_model=list[ArticleResponse])
def list_articles(limit: Annotated[int, Query(ge=1, le=100)] = 3, db: Session = Depends(get_session)):
    return (
        db.query(Article)
        .order_by(Article.created_at.desc(), Article.id.desc())
        .limit(limit)
        .all()
    )


@app.get("/api/articles/{article_id}", response_model=ArticleResponse)
def get_article(article_id: int, db: Session = Depends(get_session)):
    article = db.query(Article).filter(Article.id == article_id).first()
    if article is None:
        raise HTTPException(status_code=404, detail="Article not found")
    return article


@app.post("/api/articles", status_code=201, response_model=ArticleResponse)
def create_article(
    article: ArticleCreate,
    db: Session = Depends(get_session),
    current_user: User = Depends(get_current_user),
):
    new_article = Article(
        title=article.title,
        content=article.content,
        author_id=current_user.id,
    )
    db.add(new_article)
    db.commit()
    db.refresh(new_article)
    return new_article


@app.put("/api/articles/{article_id}", response_model=ArticleResponse)
def update_article(
    article_id: int,
    updated_article: ArticleUpdate,
    db: Session = Depends(get_session),
    current_user: User = Depends(get_current_user),
):
    article = db.query(Article).filter(Article.id == article_id).first()
    if article is None:
        raise HTTPException(status_code=404, detail="Article not found")
    if current_user.id != article.author_id:
        raise HTTPException(status_code=403, detail="You don't own this article")

    article.title = updated_article.title
    article.content = updated_article.content
    db.commit()
    db.refresh(article)
    return article


@app.delete("/api/articles/{article_id}")
def delete_article(
    article_id: int,
    db: Session = Depends(get_session),
    current_user: User = Depends(get_current_user),
):
    article = db.query(Article).filter(Article.id == article_id).first()
    if article is None:
        raise HTTPException(status_code=404, detail="Article not found")
    if current_user.id != article.author_id:
        raise HTTPException(status_code=403, detail="You don't own this article")

    db.delete(article)
    db.commit()
    return {"message": "Article deleted successfully"}
