from fastapi import FastAPI, HTTPException, Depends
from pydantic import BaseModel
from sqlalchemy.orm import Session
from database import get_session
from models import Article

app = FastAPI()


class ArticleCreate(BaseModel):
    title: str
    content: str


# In-memory storage for now — replaced by PostgreSQL once we introduce
# persistence (Phase 3). Data is lost on every server restart.
articles = []


@app.get("/api/health")
def health_check():
    return {"status": "ok"}


@app.get("/api/articles")
def list_articles(limit: int = 5, db: Session = Depends(get_session)):
    return db.query(Article).limit(limit).all()


@app.get("/api/articles/{article_id}")
def get_article(article_id: int, db: Session = Depends(get_session)):
    article = db.query(Article).filter(Article.id == article_id).first()
    if article is None:
        raise HTTPException(status_code=404, detail="Article not found")
    return article


@app.put("/api/articles/{article_id}")
def update_article(article_id: int, updated_article: ArticleCreate):
    for article in articles:
        if article["id"] == article_id:
            article['title'] = updated_article.title
            article['content'] = updated_article.content
            return article
    raise HTTPException(status_code=404, detail="Article not found")


@app.delete("/api/article/{article_id}")
def delete_article(article_id: int):
    for article in articles:
        if article["id"] == article_id:
            articles.remove(article)
            return {"message": "Article deleted sucessfully"}
    raise HTTPException(status_code=404, detail="Article not found")


@app.post("/api/articles")
def create_article(article: ArticleCreate):
    # Sequential ID is a temporary stand-in until the database
    # generates real primary keys.
    new_article = {
        "id": len(articles) + 1,
        "title": article.title,
        "content": article.content,
    }
    articles.append(new_article)
    return new_article
