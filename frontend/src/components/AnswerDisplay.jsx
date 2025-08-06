import React from "react";

const AnswerDisplay = ({ answer, sources }) => {
  if (!answer && (!sources || sources.length === 0)) {
    return null;
  }

  return (
    <div className="answer-container">
      {answer && (
        <div className="answer-section">
          <h3>💡 Answer</h3>
          <div className="answer-text">
            {answer}
          </div>
        </div>
      )}

      {sources && sources.length > 0 && (
        <div className="sources-section">
          <h4>📚 Sources ({sources.length})</h4>
          <ul className="sources-list">
            {sources.map((src, i) => (
              <li key={i} className="source-item">
                <strong>Source {i + 1}:</strong> {src}
              </li>
            ))}
          </ul>
        </div>
      )}
    </div>
  );
};

export default AnswerDisplay;