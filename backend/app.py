from fastapi import FastAPI
from backend.routers.news import router as news_router

app = FastAPI(
    title="Financial News Sentiment API",
    version="2.0"
)

app.include_router(news_router)


@app.get("/")
def home():
    return {"message": "Financial News Sentiment API is running."}


@app.get("/health")
def health():
    return {"status": "OK"}