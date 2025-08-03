import React from "react";

const AnswerDisplay = ({ answer, sources }) => {
  if (!answer && (!sources || sources.length === 0)) {
    return null; // Don't render anything if there's nothing to show
  }

  return (
    <div style={{ marginTop: "20px" }}>
      {answer && (
        <>
          <h3>Answer:</h3>
          <p>{answer}</p>
        </>
      )}

      {sources && sources.length > 0 && (
        <>
          <h4>Sources:</h4>
          <ul>
            {sources.map((src, i) => (
              <li key={i}>{src}</li>
            ))}
          </ul>
        </>
      )}
    </div>
  );
};

export default AnswerDisplay;
