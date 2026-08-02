from pydantic import BaseModel
from typing import List


class Article(BaseModel):
    headline: str
    source: str
    published: str
    sentiment: str
    url: str
    summary: str


class SentimentSummary(BaseModel):
    positive: int
    neutral: int
    negative: int


class NewsResponse(BaseModel):
    company: str
    total_articles: int
    summary: SentimentSummary
    articles: List[Article]