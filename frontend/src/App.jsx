import { useState } from "react";
import "./App.css";

function App() {
const [company, setCompany] = useState("");
const [articles, setArticles] = useState([]);
const [summary, setSummary] = useState(null);
const [loading, setLoading] = useState(false);
const [error, setError] = useState("");

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

      console.log(data);

      // Temporary
setArticles(data.articles || []);

setSummary(data.summary);
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

      <h1>Financial News Sentiment Analyzer</h1>

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

            <h3>
  <a
    href={article.url}
    target="_blank"
    rel="noreferrer"
  >
    {article.headline}
  </a>
</h3>

            <p>
              <strong>Source:</strong> {article.source}
            </p>

            <p>
              <strong>Published:</strong> {article.published}
            </p>

           <p>
  <strong>Sentiment:</strong>

  <span
    className={`badge ${article.sentiment.toLowerCase()}`}
  >
    {article.sentiment.toUpperCase()}
  </span>

</p>

          </div>

        ))}

      </div>

    </div>
  );
}

export default App;