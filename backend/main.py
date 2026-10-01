from fastapi import FastAPI, HTTPException, Depends
from pydantic import BaseModel, ConfigDict, EmailStr
from sqlalchemy.orm import Session
from sqlalchemy.exc import IntegrityError
from database import get_session
from models import Article, User
from security import get_password_hash
from datetime import datetime

app = FastAPI()


class ArticleCreate(BaseModel):
    title: str
    content: str
    # Temporally the client picks the author until authentication
    # (Phase 7) lets the server derive it from the logged-in user.
    author_id: int


class ArticleUpdate(BaseModel):
    title: str
    content: str


class ArticleResponse(BaseModel):
    id: int
    title: str
    content: str
    author_id: int
    created_at: datetime
    
    # Lets Pydantic read values from SQLAlchemy ORM objects, not only dicts
    model_config = ConfigDict(from_attributes=True)


class UserCreate(BaseModel):
    username: str
    email: EmailStr
    password: str


class UserResponse(BaseModel):
    id: int
    username: str
    email: EmailStr
    created_at: datetime

    model_config = ConfigDict(from_attributes=True)


@app.get("/api/health")
def health_check():
    return {"status": "ok"}


@app.post("/api/users", status_code=201, response_model=UserResponse)
def create_user(user: UserCreate, db: Session = Depends(get_session)):
    hashed_password = get_password_hash(user.password)

    new_user = User(username=user.username, email=user.email, password_hash=hashed_password)
    db.add(new_user)
    try:
        db.commit()
    except IntegrityError:
        # A failed commit leaves de session unusable until rolled back.
        db.rollback()
        raise HTTPException(status_code=409, detail="Username or email already exists")
    db.refresh(new_user)
    return new_user


@app.get("/api/users/{user_id}", response_model=UserResponse)
def get_user(user_id: int, db: Session = Depends(get_session)):
    user = db.query(User).filter(User.id == user_id).first()
    if user is None:
        raise HTTPException(status_code=404, detail="User not found")
    return user
    

@app.get("/api/users/{user_id}/articles", response_model=list[ArticleResponse])
def list_author_articles(user_id: int, limit: int = 10, db: Session = Depends(get_session)):
    author = db.query(User).filter(User.id == user_id).first()
    if author is None:
        raise HTTPException(status_code=404, detail="Author not found")
    return db.query(Article).filter(Article.author_id == user_id).limit(limit).all()


@app.get("/api/articles", response_model=list[ArticleResponse])
def list_articles(limit: int = 5, db: Session = Depends(get_session)):
    return db.query(Article).limit(limit).all()


@app.get("/api/articles/{article_id}", response_model=ArticleResponse)
def get_article(article_id: int, db: Session = Depends(get_session)):
    article = db.query(Article).filter(Article.id == article_id).first()
    if article is None:
        raise HTTPException(status_code=404, detail="Article not found")
    return article


@app.post("/api/articles", response_model=ArticleResponse)
def create_article(article: ArticleCreate, db: Session = Depends(get_session)):
    author = db.query(User).filter(User.id == article.author_id).first()
    if author is None:
        raise HTTPException(status_code=404, detail="Author not found")

    new_article = Article(
        title=article.title,
        content=article.content,
        author_id=article.author_id,
    )
    db.add(new_article)
    db.commit()
    db.refresh(new_article)
    return new_article


@app.put("/api/articles/{article_id}")
def update_article(article_id: int, updated_article: ArticleCreate, db: Session = Depends(get_session)):
    article = db.query(Article).filter(Article.id == article_id).first()
    if article is None:
        raise HTTPException(status_code=404, detail="Article not found")

    article.title = updated_article.title
    article.content = updated_article.content
    db.commit()
    db.refresh(article)
    return article


@app.delete("/api/article/{article_id}")
def delete_article(article_id: int, db: Session = Depends(get_session)):
    article = db.query(Article).filter(Article.id == article_id).first()
    if article is None:
        raise HTTPException(status_code=404, detail="Article not found")

    db.delete(article)
    db.commit()
    return {"message": "Article deleted successfully"}
