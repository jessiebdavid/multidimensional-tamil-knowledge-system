import { useState } from "react";
import "./App.css";

function App() {
  const [query, setQuery] = useState("");
  const [result, setResult] = useState(null);
  const [loading, setLoading] = useState(false);
  const [error, setError] = useState("");

  const analyzeQuery = async () => {
    if (!query.trim()) {
      setError("Please enter a scientific question.");
      return;
    }

    setLoading(true);
    setError("");
    setResult(null);

    try {
      const response = await fetch("/analyze", {
        method: "POST",
        headers: {
          "Content-Type": "application/json",
        },
        body: JSON.stringify({
          query: query,
        }),
      });

      if (!response.ok) {
        throw new Error("Analysis request failed.");
      }

      const data = await response.json();
      setResult(data);
    } catch (err) {
      setError(
        "Could not connect to the analysis server. Make sure FastAPI is running."
      );
    } finally {
      setLoading(false);
    }
  };

  return (
    <div className="app">
      <header className="header">
        <h1>Multidimensional Tamil Knowledge System</h1>
        <p>
          Explore relationships between scientific concepts and classical
          Tamil literature.
        </p>
      </header>

      <main className="main">
        <section className="query-section">
          <h2>Ask a Scientific Question</h2>

          <textarea
            value={query}
            onChange={(event) => setQuery(event.target.value)}
            placeholder="Example: What is time dilation?"
            rows="4"
          />

          <button onClick={analyzeQuery} disabled={loading}>
            {loading ? "Analyzing..." : "Analyze"}
          </button>

          {error && <p className="error">{error}</p>}
        </section>

        {result && (
          <section className="results-section">
            <h2>Analysis Results</h2>

            <div className="result-card">
              <h3>Scientific Concepts</h3>
              <ul>
                {result.scientific_concepts.map((concept, index) => (
                  <li key={index}>{concept}</li>
                ))}
              </ul>
            </div>

            <div className="result-card">
              <h3>Scientific Domains</h3>
              <ul>
                {result.scientific_domains.map((domain, index) => (
                  <li key={index}>{domain}</li>
                ))}
              </ul>
            </div>

            <div className="result-card">
              <h3>Dimensional Analysis</h3>

              {result.dimensional_analysis.map((item, index) => (
                <div key={index}>
                  <p>
                    <strong>Dimension:</strong> {item.dimension}
                  </p>
                  <p>
                    <strong>Concept:</strong> {item.concept}
                  </p>
                  <p>
                    <strong>Representation:</strong>{" "}
                    {item.representation_type}
                  </p>
                </div>
              ))}
            </div>

            <div className="result-card">
              <h3>Tamil Literary Evidence</h3>

              {result.tamil_evidence.map((evidence, index) => (
                <div key={index} className="evidence">
                  <p>
                    <strong>Source:</strong> {evidence.source_type}
                  </p>

                  <p>
                    <strong>ID:</strong> {evidence.source_id}
                  </p>

                  <p className="tamil-text">{evidence.text}</p>

                  <p>
                    <strong>Retrieval Score:</strong>{" "}
                    {evidence.retrieval_score.toFixed(4)}
                  </p>
                </div>
              ))}
            </div>

            <div className="result-card">
              <h3>Relationship Analysis</h3>

              <p>
                <strong>Relationship:</strong>{" "}
                {result.relationship_type}
              </p>

              <p>
                <strong>Confidence:</strong>{" "}
                {result.relationship_confidence}
              </p>

              <p>
                <strong>Reasoning:</strong> {result.reasoning}
              </p>

              <p>
                <strong>Uncertainty:</strong>{" "}
                {result.uncertainty ? "Yes" : "No"}
              </p>
            </div>
          </section>
        )}
      </main>
    </div>
  );
}

export default App;