from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware

from backend.routers.news import router as news_router
from backend.routers.stock import router as stock_router


app = FastAPI(
    title="Financial News Sentiment API",
    version="2.0"
)

# Allow React frontend to access this API
app.add_middleware(
    CORSMiddleware,
    allow_origins=[
        "http://localhost:5173",
        "http://127.0.0.1:5173",
        "https://real-time-financial-news-sentiment-iskv.onrender.com",

    ],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)


# Register API routers
app.include_router(news_router)
app.include_router(stock_router)


@app.get("/")
def home():
    return {
        "message": "Financial News Sentiment API is running."
    }


@app.get("/health")
def health():
    return {
        "status": "OK"
    }