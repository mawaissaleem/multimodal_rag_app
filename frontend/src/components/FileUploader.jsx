import React, { useState } from "react";
import { uploadFile } from "../api/api";

const FileUploader = ({ onUploadComplete }) => {
  const [file, setFile] = useState(null);
  const [status, setStatus] = useState("");

  const handleUpload = async () => {
    if (!file) return;
    setStatus("Uploading...");
    try {
      await uploadFile(file);
      setStatus("Upload successful");
      onUploadComplete();
    } catch (e) {
      setStatus("Upload failed");
    }
  };

  return (
    <div>
      <input type="file" accept=".pdf,.mp4" onChange={e => setFile(e.target.files[0])} />
      <button onClick={handleUpload}>Upload</button>
      <p>{status}</p>
    </div>
  );
};

export default FileUploader;
