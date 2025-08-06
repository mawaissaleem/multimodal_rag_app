import React, { useState } from "react";
import { uploadFile } from "../api/api";

const FileUploader = ({ onUploadComplete }) => {
  const [loading, setLoading] = useState(false);
  const [dragOver, setDragOver] = useState(false);

  const handleFileUpload = async (file) => {
    if (!file) return;
    setLoading(true);
    try {
      await uploadFile(file);
      onUploadComplete();
    } catch (error) {
      alert("Upload failed. Please try again.");
    } finally {
      setLoading(false);
    }
  };

  const handleDrop = (e) => {
    e.preventDefault();
    setDragOver(false);
    const file = e.dataTransfer.files[0];
    handleFileUpload(file);
  };

  const handleDragOver = (e) => {
    e.preventDefault();
    setDragOver(true);
  };

  const handleDragLeave = (e) => {
    e.preventDefault();
    setDragOver(false);
  };

  const handleFileSelect = (e) => {
    const file = e.target.files[0];
    handleFileUpload(file);
  };

  return (
    <div
      className={`file-uploader ${dragOver ? 'dragover' : ''}`}
      onDrop={handleDrop}
      onDragOver={handleDragOver}
      onDragLeave={handleDragLeave}
      onClick={() => document.getElementById('file-input').click()}
    >
      <input
        id="file-input"
        type="file"
        className="file-input"
        onChange={handleFileSelect}
        accept=".pdf,.doc,.docx,.txt,.png,.jpg,.jpeg"
      />
      
      <div className="upload-content">
        <h3>📁 Upload Document</h3>
        <p>Drag and drop your file here, or click to browse</p>
        <p style={{ fontSize: '0.9rem', color: '#999' }}>
          Supports: PDF, DOC, DOCX, TXT, PNG, JPG, JPEG
        </p>
        
        <button 
          className="upload-button" 
          disabled={loading}
          onClick={(e) => e.stopPropagation()}
        >
          {loading ? (
            <div className="loading-spinner">
              <div className="spinner"></div>
              Uploading...
            </div>
          ) : (
            'Choose File'
          )}
        </button>
      </div>
    </div>
  );
};

export default FileUploader;