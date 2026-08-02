import { useState } from "react";
import "./App.css";

function App() {
const [company, setCompany] = useState("");
const [articles, setArticles] = useState([]);
const [summary, setSummary] = useState(null);
const [loading, setLoading] = useState(false);
const [error, setError] = useState("");
const [searchedCompany, setSearchedCompany] = useState("");
const [totalArticles, setTotalArticles] = useState(0);
const [companyInfo, setCompanyInfo] = useState(null);
const [overallSentiment, setOverallSentiment] = useState("");

  const searchNews = async () => {
    if (!company.trim()) {
  setError("Please enter a company name.");
  return;
}

setError("");

    setLoading(true);

    try {
      const response = await fetch(
        `http://127.0.0.1:8000/news/${company}`
      );

      const data = await response.json();
      setCompanyInfo({
  company: data.company,
  total: data.total_articles,
});
      setSearchedCompany(data.company);
      setTotalArticles(data.total_articles);
      console.log(data);

      {companyInfo && (
  <div className="company-banner">

    <h2>{companyInfo.company}</h2>

    <p>
      {companyInfo.total} Articles Analyzed
    </p>

  </div>
)}
      // Temporary
setArticles(data.articles || []);

setSummary(data.summary);
const { positive, neutral, negative } = data.summary;

if (positive > neutral && positive > negative) {
  setOverallSentiment("POSITIVE");
} else if (negative > positive && negative > neutral) {
  setOverallSentiment("NEGATIVE");
} else {
  setOverallSentiment("NEUTRAL");
}
console.log("Summary:", data.summary);

    } catch (error) {
      console.error(error);
    }
    finally {
setLoading(false);
    }
  };

  return (
    <div className="container">


      <h1 className="title">
  📈 Financial News Sentiment Dashboard
</h1>

<p className="subtitle">
  AI Powered Market Intelligence
</p>

{searchedCompany && (
  <div className="company-info">
    <h2>{searchedCompany}</h2>
    <p>{totalArticles} Articles Found</p>
  </div>
)}
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

  <button
    onClick={searchNews}
    disabled={loading}
  >
    {loading ? "Searching..." : "Search"}
  </button>

</div>

{/* Error Message */}
{error && (
  <p className="error">
    {error}
  </p>
)}

{/* Loading Message */}
{loading && (
  <p className="loading">
    Searching latest financial news...
  </p>
)}

{overallSentiment && (
  <div className="overall-card">

    <h2>Overall Market Sentiment</h2>

    <div className={`overall-badge ${overallSentiment.toLowerCase()}`}>
      {overallSentiment}
    </div>

    <p>
      Based on analysis of {companyInfo?.total} news articles
    </p>

  </div>
)}

{/* Summary Cards */}
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

<div className="results">

        {articles.map((article, index) => (

  <div className="card" key={index}>

    <h3>{article.headline}</h3>

    <div className="meta">

      <span>📰 {article.source}</span>

      <span>🕒 {article.published}</span>

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