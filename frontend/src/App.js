import React, { useState } from "react";
import FileUploader from "./components/FileUploader";
import QueryInput from "./components/QueryInput";
import AnswerDisplay from "./components/AnswerDisplay";

const App = () => {
  const [answer, setAnswer] = useState("");
  const [sources, setSources] = useState([]);

  const handleResult = (res) => {
    setAnswer(res.answer);
    setSources(res.sources || []);
  };

  return (
    <div style={{ maxWidth: "600px", margin: "auto" }}>
      <h1>Multimodal RAG App</h1>
      <FileUploader onUploadComplete={() => alert("File uploaded")} />
      <QueryInput onResult={handleResult} />
      <AnswerDisplay answer={answer} sources={sources} />
    </div>
  );
};

export default App;
