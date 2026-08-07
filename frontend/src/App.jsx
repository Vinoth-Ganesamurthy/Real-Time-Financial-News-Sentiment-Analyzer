import { useState } from "react";
import "./App.css";

function App() {
  const [company, setCompany] = useState("");
  const [limit, setLimit] = useState(5);

  const [articles, setArticles] = useState([]);
  const [summary, setSummary] = useState(null);

  const [loading, setLoading] = useState(false);
  const [error, setError] = useState("");

  const [searchedCompany, setSearchedCompany] = useState("");
  const [totalArticles, setTotalArticles] = useState(0);

  const [companyInfo, setCompanyInfo] = useState(null);

  const [overallSentiment, setOverallSentiment] = useState("");

  // Stock data
  const [stockData, setStockData] = useState(null);

  const searchNews = async () => {
    if (!company.trim()) {
      setError("Please enter a company name.");
      return;
    }

    setError("");
    setLoading(true);

    try {
      // Fetch news and stock data together
      const [newsResponse, stockResponse] = await Promise.all([
        fetch(`/news/${company}?limit=${limit}`),
        fetch(`/stock/${company}`),
      ]);

      const newsData = await newsResponse.json();

      // -------------------------
      // NEWS RESPONSE
      // -------------------------

      if (!newsResponse.ok) {
        setError(newsData.detail || "Something went wrong.");
        setArticles([]);
        setSummary(null);
        setCompanyInfo(null);
        setStockData(null);
        setOverallSentiment("");
        return;
      }

      setCompanyInfo({
        company: newsData.company,
        total: newsData.total_articles,
      });

      setSearchedCompany(newsData.company);
      setTotalArticles(newsData.total_articles);

      setArticles(newsData.articles || []);
      setSummary(newsData.summary);

      // Calculate overall sentiment
      const { positive, neutral, negative } = newsData.summary;

      if (positive > neutral && positive > negative) {
        setOverallSentiment("POSITIVE");
      } else if (negative > positive && negative > neutral) {
        setOverallSentiment("NEGATIVE");
      } else {
        setOverallSentiment("NEUTRAL");
      }

      // -------------------------
      // STOCK RESPONSE
      // -------------------------

      if (stockResponse.ok) {
        const stock = await stockResponse.json();

        setStockData(stock);
      } else {
        setStockData(null);
      }
    } catch (err) {
      console.error(err);

      setError("Unable to connect to server.");
      setArticles([]);
      setSummary(null);
      setStockData(null);
    } finally {
      setLoading(false);
    }
  };

  return (
    <div className="container">

      {/* HEADER */}

      <h1 className="title">
        📈 Financial News Sentiment Dashboard
      </h1>

      <p className="subtitle">
        AI Powered Market Intelligence
      </p>

      {/* SEARCH */}

      <div className="search-box">

        <input
          type="text"
          placeholder="Enter Company Name..."
          value={company}
          onChange={(e) => setCompany(e.target.value)}
          onKeyDown={(e) => {
            if (e.key === "Enter") {
              searchNews();
            }
          }}
        />

        <select
  value={limit}
  onChange={(e) => setLimit(Number(e.target.value))}
  onKeyDown={(e) => {
    if (e.key === "Enter") {
      e.preventDefault();
      searchNews();
    }
  }}
>
  <option value={5}>5 Articles</option>
  <option value={10}>10 Articles</option>
  <option value={20}>20 Articles</option>
  <option value={50}>50 Articles</option>
        </select>
        <button
          onClick={searchNews}
          disabled={loading}
        >
          {loading ? "Searching..." : "Search"}
        </button>

      </div>

      {/* ERROR */}

      {error && (
        <p className="error">
          {error}
        </p>
      )}

      {/* LOADING */}

      {loading && (
        <p className="loading">
          Fetching latest market data and financial news...
        </p>
      )}

      {/* COMPANY INFO */}

      {companyInfo && (
        <div className="company-info">

          <h2>{companyInfo.company}</h2>

          <p>
            {companyInfo.total} Articles Found
          </p>

        </div>
      )}

      {/* STOCK OVERVIEW */}

      {stockData && (
        <div className="stock-card">

          <div className="stock-header">

            <div>
              <h2>{stockData.company}</h2>

              <span className="stock-symbol">
                {stockData.symbol}
              </span>
            </div>

            <div className="stock-price">

              <h2>
                ${stockData.current_price?.toFixed(2)}
              </h2>

              <span
                className={
                  stockData.change >= 0
                    ? "stock-positive"
                    : "stock-negative"
                }
              >
                {stockData.change >= 0 ? "+" : ""}
                ${stockData.change?.toFixed(2)}
                {" "}
                ({stockData.change_percent?.toFixed(2)}%)
              </span>

            </div>

          </div>

          <div className="stock-details">

            <div>
              <span>Day High</span>
              <strong>
                ${stockData.day_high?.toFixed(2)}
              </strong>
            </div>

            <div>
              <span>Day Low</span>
              <strong>
                ${stockData.day_low?.toFixed(2)}
              </strong>
            </div>

            <div>
              <span>Previous Close</span>
              <strong>
                ${stockData.previous_close?.toFixed(2)}
              </strong>
            </div>

          </div>

        </div>
      )}

      {/* OVERALL SENTIMENT */}

      {overallSentiment && (
        <div className="overall-card">

          <h2>Overall Market Sentiment</h2>

          <div
            className={`overall-badge ${overallSentiment.toLowerCase()}`}
          >
            {overallSentiment}
          </div>

          <p>
            Based on analysis of {companyInfo?.total} news articles
          </p>

        </div>
      )}

      {/* SENTIMENT SUMMARY */}

      {summary && (
        <div className="summary">

          <div className="summary-card positive">
            <h2>{summary.positive}</h2>
            <p>Positive</p>
          </div>

          <div className="summary-card neutral">
            <h2>{summary.neutral}</h2>
            <p>Neutral</p>
          </div>

          <div className="summary-card negative">
            <h2>{summary.negative}</h2>
            <p>Negative</p>
          </div>

        </div>
      )}

      {/* NEWS ARTICLES */}

      <div className="results">

        {articles.map((article, index) => (

          <div className="card" key={index}>

            <h3>{article.headline}</h3>

            <div className="meta">

              <span>
                📰 {article.source}
              </span>

              <span>
                🕒 {article.published}
              </span>

            </div>

            <div className="sentiment-row">

              <span
                className={`badge ${article.sentiment.toLowerCase()}`}
              >
                {article.sentiment.toUpperCase()}
              </span>

            </div>

            <a
              className="read-more"
              href={article.url}
              target="_blank"
              rel="noreferrer"
            >
              Read Full Article →
            </a>

          </div>

        ))}

      </div>

    </div>
  );
}

export default App;