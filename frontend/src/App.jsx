import { useState } from "react";
import "./App.css";

function App() {
  const [company, setCompany] = useState("");
  const [data, setData] = useState(null);

  const searchNews = async () => {
    if (!company) return;

    try {
      const response = await fetch(
        `http://127.0.0.1:8000/news/${company}`
      );

      const result = await response.json();

      console.log(result);

      setData(result);

    } catch (error) {
      console.error(error);
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
        />

        <button onClick={searchNews}>
          Search
        </button>
      </div>

      {data && (
        <pre style={{ marginTop: "40px", textAlign: "left" }}>
          {JSON.stringify(data, null, 2)}
        </pre>
      )}
    </div>
  );
}

export default App;