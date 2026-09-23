from fastapi import FastAPI

app = FastAPI()

@app.get("/api/health")
def health_check():
    return {"status": "ok"}

@app.get("/api/greet/{name}")
def greet(name: str):
    return {"message": f"Hello, {name.title()}"}

@app.get("/api/articles")
def list_articles(limit: int = 5):
    return {"limit": limit, "articles": []}
