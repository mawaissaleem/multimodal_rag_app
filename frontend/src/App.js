import React, { useState } from "react";
import FileUploader from "./components/FileUploader";
import QueryInput from "./components/QueryInput";
import AnswerDisplay from "./components/AnswerDisplay";
import "./App.css";

const App = () => {
  const [answer, setAnswer] = useState("");
  const [sources, setSources] = useState([]);

  const handleResult = (res) => {
    setAnswer(res.answer);
    setSources(res.sources || []);
  };

  return (
    <div className="app-container">
      <div className="main-content">
        <header className="app-header">
          <h1>Multimodal RAG</h1>
          <p>Upload documents and ask questions to get AI-powered answers</p>
        </header>
        
        <div className="upload-section">
          <FileUploader onUploadComplete={() => alert("File uploaded successfully!")} />
        </div>
        
        <div className="query-section">
          <QueryInput onResult={handleResult} />
        </div>
        
        <div className="results-section">
          <AnswerDisplay answer={answer} sources={sources} />
        </div>
      </div>
    </div>
  );
};

export default App;