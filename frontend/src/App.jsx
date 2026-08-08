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

  const [stockPerformance, setStockPerformance] = useState(null);

  const searchNews = async () => {
    if (!company.trim()) {
      setError("Please enter a company name.");
      return;
    }

    setError("");
    setLoading(true);

    try {
      // -----------------------------
      // Fetch News
      // -----------------------------

      const newsResponse = await fetch(
        `/news/${encodeURIComponent(company.trim())}?limit=${limit}`
      );

      const newsData = await newsResponse.json();

      if (!newsResponse.ok) {
        setError(newsData.detail || "Something went wrong.");

        setArticles([]);
        setSummary(null);
        setCompanyInfo(null);
        setStockPerformance(null);
        setOverallSentiment("");

        return;
      }

      // -----------------------------
      // Company Information
      // -----------------------------

      setCompanyInfo({
        company: newsData.company,
        total: newsData.total_articles,
      });

      setSearchedCompany(newsData.company);
      setTotalArticles(newsData.total_articles);

      // -----------------------------
      // Articles
      // -----------------------------

      setArticles(newsData.articles || []);

      // -----------------------------
      // Sentiment Summary
      // -----------------------------

      setSummary(newsData.summary);

      const {
        positive,
        neutral,
        negative,
      } = newsData.summary;

      if (positive > neutral && positive > negative) {
        setOverallSentiment("POSITIVE");
      } else if (negative > positive && negative > neutral) {
        setOverallSentiment("NEGATIVE");
      } else {
        setOverallSentiment("NEUTRAL");
      }

      // -----------------------------
      // Fetch Stock Performance
      // -----------------------------

      const performanceResponse = await fetch(
        `/stock/performance/${encodeURIComponent(company.trim())}`
      );

      const performanceData = await performanceResponse.json();

      if (performanceResponse.ok) {
        setStockPerformance(performanceData);
      } else {
        setStockPerformance(null);
      }

    } catch (err) {
      console.error(err);

      setError("Unable to connect to server.");

      setArticles([]);
      setSummary(null);
      setCompanyInfo(null);
      setStockPerformance(null);
      setOverallSentiment("");
    } finally {
      setLoading(false);
    }
  };

  return (
    <div className="container">

      {/* ----------------------------- */}
      {/* Header */}
      {/* ----------------------------- */}

      <h1 className="title">
        📈 Financial News Sentiment Dashboard
      </h1>

      <p className="subtitle">
        AI Powered Market Intelligence
      </p>

      {/* ----------------------------- */}
      {/* Company Information */}
      {/* ----------------------------- */}

      {companyInfo && (
        <div className="company-info">

          <h2>
            {searchedCompany}
          </h2>

          <p>
            {totalArticles} Articles Found
          </p>

        </div>
      )}

      {/* ----------------------------- */}
      {/* Search */}
      {/* ----------------------------- */}

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
      e.stopPropagation();
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

      {/* ----------------------------- */}
      {/* Error */}
      {/* ----------------------------- */}

      {error && (
        <p className="error">
          {error}
        </p>
      )}

      {/* ----------------------------- */}
      {/* Loading */}
      {/* ----------------------------- */}

      {loading && (
        <p className="loading">
          Searching latest financial news and stock data...
        </p>
      )}

      {/* ----------------------------- */}
      {/* Stock Performance */}
      {/* ----------------------------- */}

      {stockPerformance && (
        <div className="stock-performance">

          <h2>
            📊 Stock Performance
          </h2>

          <div className="performance-grid">

            <div className="performance-card">
              <h3>Current Price</h3>
              <p>
                ${stockPerformance.current_price}
              </p>
            </div>

            <div className="performance-card">
              <h3>1 Week</h3>
              <p
                className={
                  stockPerformance.one_week_return >= 0
                    ? "positive-value"
                    : "negative-value"
                }
              >
                {stockPerformance.one_week_return >= 0 ? "+" : ""}
                {stockPerformance.one_week_return}%
              </p>
            </div>

            <div className="performance-card">
              <h3>1 Month</h3>
              <p
                className={
                  stockPerformance.one_month_return >= 0
                    ? "positive-value"
                    : "negative-value"
                }
              >
                {stockPerformance.one_month_return >= 0 ? "+" : ""}
                {stockPerformance.one_month_return}%
              </p>
            </div>

            <div className="performance-card">
              <h3>3 Months</h3>
              <p
                className={
                  stockPerformance.three_month_return >= 0
                    ? "positive-value"
                    : "negative-value"
                }
              >
                {stockPerformance.three_month_return >= 0 ? "+" : ""}
                {stockPerformance.three_month_return}%
              </p>
            </div>

            <div className="performance-card">
              <h3>Annualized Volatility</h3>
              <p>
                {stockPerformance.annualized_volatility}%
              </p>
            </div>

            <div className="performance-card">
              <h3>Maximum Drawdown</h3>
              <p className="negative-value">
                {stockPerformance.maximum_drawdown}%
              </p>
            </div>

          </div>

        </div>
      )}

      {/* ----------------------------- */}
      {/* Overall Sentiment */}
      {/* ----------------------------- */}

      {overallSentiment && (
        <div className="overall-card">

          <h2>
            Overall Market Sentiment
          </h2>

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

      {/* ----------------------------- */}
      {/* Summary Cards */}
      {/* ----------------------------- */}

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

      {/* ----------------------------- */}
      {/* News Articles */}
      {/* ----------------------------- */}

      <div className="results">

        {articles.map((article, index) => (

          <div
            className="card"
            key={`${article.url}-${index}`}
          >

            <h3>
              {article.headline}
            </h3>

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