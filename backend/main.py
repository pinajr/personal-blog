from fastapi import FastAPI, HTTPException
from pydantic import BaseModel

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
def list_articles(limit: int = 5):
    return {"limit": limit, "articles": articles[:limit]}


@app.get("/api/articles/{article_id}")
def get_article(article_id: int):
    for article in articles:
        if article["id"] == article_id:
            return article
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
