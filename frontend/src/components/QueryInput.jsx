import React, { useState } from "react";
import { sendQuery } from "../api/api";

const QueryInput = ({ onResult }) => {
  const [query, setQuery] = useState("");
  const [loading, setLoading] = useState(false);

  const handleQuery = async () => {
    if (!query.trim()) return;
    setLoading(true);
    try {
      const result = await sendQuery(query);
      onResult(result);
    } catch {
      onResult({ answer: "Failed to fetch answer.", sources: [] });
    } finally {
      setLoading(false);
    }
  };

  return (
    <div>
      <textarea
        placeholder="Ask a question..."
        value={query}
        onChange={e => setQuery(e.target.value)}
      />
      <button onClick={handleQuery} disabled={loading}>
        {loading ? "Loading..." : "Ask"}
      </button>
    </div>
  );
};

export default QueryInput;
