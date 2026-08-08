# 📈 Real-Time Financial News Sentiment Analyzer

A full-stack financial analytics application that combines **real-time financial news, machine-learning-based sentiment analysis, and historical stock performance metrics** in a responsive web dashboard.

The application allows users to search for a company, retrieve recent relevant financial news, classify each headline as **Positive, Neutral, or Negative**, and simultaneously view historical stock-performance and risk metrics.

The project supports companies across multiple international markets, including the **United States, India, Singapore, and Australia**.

---

## 🌐 Live Application

### 🚀 Live Dashboard

👉 **https://real-time-financial-news-sentiment-iskv.onrender.com**

### 📚 FastAPI Swagger Documentation

👉 **https://real-time-financial-news-sentiment.onrender.com/docs**

### ⚙️ Backend API

👉 **https://real-time-financial-news-sentiment.onrender.com**

> **Note:** The application is hosted on Render. If the backend instance has been inactive, the first request may take longer while the service starts. Subsequent requests should be faster.

---

## 📌 Project Overview

Financial markets react continuously to company announcements, earnings reports, partnerships, acquisitions, analyst opinions, industry developments, and other news.

Reading and evaluating large numbers of articles manually can be time-consuming.

This project provides an automated workflow that:

1. Accepts a company name from the user.
2. Resolves the company to its stock-market symbol.
3. Retrieves recent company-related financial news.
4. Filters irrelevant and duplicate articles.
5. Uses a trained machine-learning model to classify news sentiment.
6. Calculates an overall market sentiment summary.
7. Retrieves historical stock-price data.
8. Calculates stock performance and risk metrics.
9. Presents the results through a React dashboard.

---

## ✨ Key Features

### 📰 Financial News Retrieval

The application retrieves recent company-related financial news using:

- **Finnhub**
- **NewsAPI**

The service uses different retrieval strategies depending on the market and API availability.

News results are filtered to improve company relevance and reduce unrelated articles.

---

### 🤖 Machine Learning Sentiment Analysis

Financial headlines are classified into three sentiment categories:

- 🟢 **Positive**
- 🟡 **Neutral**
- 🔴 **Negative**

The sentiment pipeline uses:

- TF-IDF text vectorization
- A trained machine-learning classification model
- Label encoding
- Saved model artifacts loaded with Joblib

The model analyzes the retrieved financial headlines and produces both article-level sentiment and an overall sentiment summary.

---

### 📊 Market Sentiment Summary

After analyzing the selected news articles, the application displays:

- Number of positive articles
- Number of neutral articles
- Number of negative articles
- Overall market mood

This provides a quick view of the recent news sentiment surrounding a company.

---

### 📈 Historical Stock Performance

The dashboard also retrieves historical market data and calculates:

- **Current Price**
- **1-Week Return**
- **1-Month Return**
- **3-Month Return**
- **Annualized Volatility**
- **Maximum Drawdown**

These metrics allow users to compare recent news sentiment with actual stock-price behavior.

---

## 🌍 Multi-Market Support

The application has been tested with companies from multiple stock exchanges.

| Market | Example Companies | Example Symbols |
|---|---|---|
| 🇺🇸 United States | Tesla, NVIDIA | `TSLA`, `NVDA` |
| 🇮🇳 India | Reliance Industries, Infosys | `RELIANCE.NS`, `INFY.NS` |
| 🇸🇬 Singapore | DBS Group, ST Engineering | `D05.SI`, `S63.SI` |
| 🇦🇺 Australia | Commonwealth Bank of Australia | `CBA.AX` |

The application also displays market-appropriate currency symbols for supported exchanges.

Examples:

```text
US           → $
India        → ₹
Singapore    → S$
Australia    → A$
```

---

## 🔄 Application Flow

```text
                         USER
                           │
                           ▼
                  React Web Dashboard
                           │
                           │ Company Name
                           ▼
                    FastAPI Backend
                           │
             ┌─────────────┴─────────────┐
             │                           │
             ▼                           ▼
      Company Resolution          Stock Data Service
             │                           │
             ▼                           ▼
        Stock Symbol               Historical Prices
             │                           │
             │                           ▼
             │                  Performance Metrics
             │
             ▼
       Financial News
             │
       ┌─────┴─────┐
       │           │
       ▼           ▼
    Finnhub     NewsAPI
       │           │
       └─────┬─────┘
             │
             ▼
     Relevance Filtering
             │
             ▼
      Duplicate Removal
             │
             ▼
       Selected Articles
             │
             ▼
       TF-IDF Vectorizer
             │
             ▼
     ML Sentiment Model
             │
             ▼
 Positive / Neutral / Negative
             │
             ▼
     Sentiment Aggregation
             │
             └──────────────┐
                            │
             Performance ───┤
                            ▼
                    JSON API Response
                            │
                            ▼
                   React Dashboard
```

---

## 🏗️ System Architecture

The application follows a full-stack service-oriented architecture.

```text
┌─────────────────────────────────────┐
│             React Frontend          │
│                                     │
│ Search                              │
│ Article Limit                       │
│ Sentiment Summary                   │
│ Stock Performance                   │
│ News Cards                          │
└─────────────────┬───────────────────┘
                  │
                  │ HTTP / JSON
                  ▼
┌─────────────────────────────────────┐
│             FastAPI Backend         │
│                                     │
│ REST Endpoints                      │
│ Company Lookup                      │
│ News Coordination                   │
│ Stock Performance                   │
│ Sentiment Prediction                │
└──────────┬───────────┬──────────────┘
           │           │
           ▼           ▼
     External APIs    ML Model
           │
     ┌─────┼─────┐
     │     │     │
 Finnhub NewsAPI Market Data
```

---

## 🧰 Technology Stack

### Frontend

- React
- Vite
- JavaScript
- HTML5
- CSS3

### Backend

- Python
- FastAPI
- Uvicorn
- Requests
- python-dotenv

### Machine Learning

- scikit-learn
- TF-IDF Vectorization
- Joblib
- NumPy
- Pandas

### Financial Data & News

- Finnhub API
- NewsAPI
- yfinance

### Deployment

- Render Web Service — FastAPI backend
- Render Static Site — React frontend
- GitHub — source control and deployment integration

---

## 🔌 API Endpoints

Interactive API documentation is available at:

**https://real-time-financial-news-sentiment.onrender.com/docs**

### API Status

```http
GET /
```

Returns the API status message.

---

### Health Check

```http
GET /health
```

Used to verify that the backend service is running.

---

### Company News & Sentiment

```http
GET /news/{company}
```

Example:

```http
GET /news/Tesla?limit=5
```

This endpoint retrieves relevant financial news and performs sentiment analysis.

---

### Stock Performance

```http
GET /stock/performance/{company}
```

Example:

```http
GET /stock/performance/Reliance
```

The response contains metrics such as:

```json
{
  "company": "Reliance",
  "symbol": "RELIANCE.NS",
  "current_price": 1334.8,
  "one_week_return": 2.06,
  "one_month_return": 4.3,
  "three_month_return": -1.16,
  "annualized_volatility": 22.66,
  "maximum_drawdown": -13.99
}
```

---

## 📰 News Retrieval Strategy

News retrieval is designed to account for differences in API market coverage.

### US Stocks

For supported US companies:

```text
Company
   ↓
Finnhub
   ↓
Relevant News
```

If appropriate news is unavailable, the application can fall back to NewsAPI.

### International Stocks

For markets where Finnhub company-news access may be unavailable or restricted:

```text
Company
   ↓
NewsAPI
   ↓
Relevance Scoring
   ↓
Duplicate Removal
   ↓
Selected Articles
```

This is particularly useful for stocks from markets such as India, Singapore, and Australia.

---

## 🎯 News Relevance Filtering

A general news search can return articles that mention a company only incidentally.

To improve sentiment quality, the application applies relevance filtering based on company-specific search terms.

Signals can include company references in:

- Headline
- Description
- Article content

The pipeline also removes duplicate results and filters low-quality or overly broad market headlines where appropriate.

This helps prevent unrelated news from influencing the sentiment calculation.

---

## 🔢 Article Limit

Users can select the maximum number of articles to analyze.

For example:

```text
Up to 5 Articles
Up to 10 Articles
Up to 20 Articles
Up to 50 Articles
```

The selected value represents the **maximum requested number of relevant articles**.

If only three relevant articles are available, the application returns three rather than filling the remaining positions with unrelated news.

This prioritizes relevance over quantity.

---

## 📐 Stock Performance Calculations

The stock analytics service calculates several useful metrics.

### Stock Return

Stock return measures percentage price change over a selected period.

```text
Return (%) =
(Current Price - Previous Price)
-------------------------------- × 100
          Previous Price
```

Returns are calculated for:

- 1 week
- 1 month
- 3 months

---

### Annualized Volatility

Annualized volatility estimates the variability of stock returns over time.

Higher volatility generally indicates larger price fluctuations.

---

### Maximum Drawdown

Maximum drawdown measures the largest decline from a historical peak to a subsequent trough during the analyzed period.

It provides a simple measure of downside risk.

---

## 💻 Local Installation

### 1. Clone the Repository

```bash
git clone <your-repository-url>
cd Real-Time-Financial-News-Sentiment-Analyzer
```

---

### 2. Create a Python Virtual Environment

Windows:

```bash
python -m venv .venv
.venv\Scripts\activate
```

macOS/Linux:

```bash
python3 -m venv .venv
source .venv/bin/activate
```

---

### 3. Install Python Dependencies

```bash
pip install -r requirements.txt
```

---

### 4. Configure Environment Variables

Create a `.env` file in the project root:

```env
FINNHUB_API_KEY=your_finnhub_api_key
NEWS_API_KEY=your_newsapi_key
```

> Never commit the `.env` file or API keys to GitHub.

---

### 5. Start the FastAPI Backend

From the project root:

```bash
uvicorn backend.app:app --reload
```

The backend will run locally at:

```text
http://127.0.0.1:8000
```

Swagger documentation:

```text
http://127.0.0.1:8000/docs
```

---

### 6. Install Frontend Dependencies

Open another terminal:

```bash
cd frontend
npm install
```

---

### 7. Start the React Frontend

```bash
npm run dev
```

The frontend will normally run at:

```text
http://localhost:5173
```

---

## ⚙️ Frontend API Configuration

The frontend supports an environment-based backend URL.

```env
VITE_API_BASE_URL=https://your-backend-domain.com
```

In production, the deployed frontend communicates with the Render-hosted FastAPI backend using this environment variable.

For local development, the existing Vite development configuration can route requests to the local backend.

---

## 🔐 Security

API credentials are stored using environment variables.

The project `.env` file should remain excluded through `.gitignore`.

Production API keys are configured directly through Render environment variables rather than being committed to the repository.

Required backend variables:

```env
FINNHUB_API_KEY=...
NEWS_API_KEY=...
```

Frontend production variable:

```env
VITE_API_BASE_URL=...
```

---

## 🚀 Production Deployment

### Backend

The FastAPI backend is deployed as a **Render Web Service**.

Build command:

```bash
pip install -r requirements.txt
```

Start command:

```bash
uvicorn backend.app:app --host 0.0.0.0 --port $PORT
```

Backend:

**https://real-time-financial-news-sentiment.onrender.com**

Swagger:

**https://real-time-financial-news-sentiment.onrender.com/docs**

---

### Frontend

The React application is deployed as a **Render Static Site**.

Root directory:

```text
frontend
```

Build command:

```bash
npm install && npm run build
```

Publish directory:

```text
dist
```

Production environment variable:

```env
VITE_API_BASE_URL=https://real-time-financial-news-sentiment.onrender.com
```

Live dashboard:

**https://real-time-financial-news-sentiment-iskv.onrender.com**

---

## 🌐 CORS Configuration

Because the frontend and backend are deployed separately, the FastAPI backend allows requests from the appropriate frontend origins.

Development origins include:

```text
http://localhost:5173
http://127.0.0.1:5173
```

Production origin:

```text
https://real-time-financial-news-sentiment-iskv.onrender.com
```

This allows the deployed React application to securely communicate with the FastAPI API.

---

## 🧪 Example Companies to Test

Try the live application with:

```text
Tesla
NVIDIA
Reliance
Infosys
DBS
Commonwealth Bank
ST Engineering
```

These examples demonstrate the application's multi-market capabilities.

---

## 📊 Example Workflow

Searching for:

```text
Reliance
```

produces a workflow similar to:

```text
Reliance
   ↓
RELIANCE.NS
   ↓
Historical Stock Data
   ↓
Stock Performance Metrics

        +

NewsAPI
   ↓
Reliance-Relevant Articles
   ↓
Relevance Filtering
   ↓
ML Sentiment Classification
   ↓
Positive / Neutral / Negative
   ↓
Overall Sentiment Summary
   ↓
React Dashboard
```

---

## ⚠️ Limitations

The application has several practical limitations:

- News availability depends on third-party API coverage.
- Some companies may have fewer relevant recent articles than the requested article limit.
- Finnhub access varies by market and API subscription level.
- Company aliases may occasionally be required when external APIs use different company names.
- Financial sentiment does not necessarily predict future stock-price movement.
- Historical performance does not guarantee future returns.
- Free hosting instances may require a short startup period after inactivity.

---

## 🔮 Future Improvements

Potential future enhancements include:

- Interactive historical stock-price charts
- Sentiment trends over time
- Additional international exchanges
- Larger dynamic company-symbol database
- Improved entity-based news relevance detection
- Transformer-based financial sentiment models such as FinBERT
- News-source weighting
- Article-level sentiment confidence visualization
- Company comparison
- Portfolio sentiment monitoring
- Watchlists
- User authentication
- Database-backed historical sentiment storage
- Automated model retraining
- Docker deployment
- Automated testing and CI/CD

---

## 🎓 Project Highlights

This project demonstrates practical experience with:

- Full-stack application development
- REST API development with FastAPI
- React frontend development
- Machine-learning model integration
- NLP-based financial sentiment analysis
- Financial market data processing
- External API integration
- Multi-market stock-symbol handling
- Data filtering and relevance scoring
- Historical stock analytics
- Environment-variable management
- CORS configuration
- Git/GitHub version control
- Cloud deployment with Render

---

## ⚖️ Disclaimer

This project is intended for **educational and analytical purposes only**.

The sentiment classifications, stock metrics, and other information displayed by the application should **not be considered financial or investment advice**.

Users should conduct independent research and consult qualified financial professionals before making investment decisions.

---

## 👩‍💻 Author

**Vinoth Ganesamurthy**

https://www.linkedin.com/in/vinoth-ganesamurthy/

Developed as a full-stack financial analytics and machine-learning portfolio project.

---

## ⭐ Support

If you find this project useful, consider giving the repository a ⭐ on GitHub.

### Live Demo

**https://real-time-financial-news-sentiment-iskv.onrender.com**

### API Documentation

**https://real-time-financial-news-sentiment.onrender.com/docs**

## 📄 License

This project is licensed under the **MIT License**.

See the `LICENSE` file for details.