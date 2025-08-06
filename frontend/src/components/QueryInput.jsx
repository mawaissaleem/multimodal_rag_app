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

  const handleKeyPress = (e) => {
    if (e.key === 'Enter' && e.ctrlKey) {
      handleQuery();
    }
  };

  return (
    <div className="query-container">
      <h3 style={{ color: '#667eea', marginBottom: '16px', fontSize: '1.3rem' }}>
        🤖 Ask a Question
      </h3>
      
      <textarea
        className="query-textarea"
        placeholder="Ask a question about your uploaded document... (Ctrl+Enter to submit)"
        value={query}
        onChange={e => setQuery(e.target.value)}
        onKeyPress={handleKeyPress}
      />
      
      <button 
        className="query-button" 
        onClick={handleQuery} 
        disabled={loading || !query.trim()}
      >
        {loading ? (
          <div className="loading-spinner">
            <div className="spinner"></div>
            Processing...
          </div>
        ) : (
          '🚀 Ask Question'
        )}
      </button>
      
      {query.trim() && (
        <p style={{ 
          fontSize: '0.85rem', 
          color: '#666', 
          marginTop: '8px',
          fontStyle: 'italic'
        }}>
          Tip: Press Ctrl+Enter to submit quickly
        </p>
      )}
    </div>
  );
};

export default QueryInput;