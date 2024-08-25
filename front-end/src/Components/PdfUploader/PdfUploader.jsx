import React, { useState } from "react";
import "./PdfUploader.css";

function PdfUploader() {
  const [selectedFiles, setSelectedFiles] = useState([]);

  const handleFileChange = (event) => {
    setSelectedFiles(Array.from(event.target.files));
  };

  const handleFileUpload = () => {
    if (selectedFiles.length > 0) {
      console.log("Files uploaded:", selectedFiles);
      // Add logic here to handle the uploaded files, e.g., upload to server or display
    }
  };

  const handleDrop = (event) => {
    event.preventDefault();
    const files = Array.from(event.dataTransfer.files).filter(file => file.type === "application/pdf");
    setSelectedFiles(prevFiles => [...prevFiles, ...files]);
  };

  const handleDragOver = (event) => {
    event.preventDefault();
  };

  const handleCancel = () => {
    setSelectedFiles([]);
  }

  return (
    <div>
      <input
        type="file"
        accept=".pdf"
        multiple
        onChange={handleFileChange}
        style={{ display: "none" }}
        id="file-input"
      />
      <label className="file-input-label"
        htmlFor="file-input"
        onDrop={handleDrop}
        onDragOver={handleDragOver}
      >
        Drag and drop your PDFs here or click to select files <br/><br/> <i class="fa-solid fa-upload bounce fa-2xl"></i>
      </label>
      
      {selectedFiles.length > 0 && (
        <ul className="pdfs">
          {selectedFiles.map((file, index) => (
            <li key={index}><i class="fa-solid fa-file-pdf" style={{color: "#da1010"}}></i> {file.name}</li>
          ))}
        </ul>
      )}
      <div className="buttons">
      <button className="upload-btn" onClick={handleFileUpload} style={{marginBottom: "10px"}}>Upload CVs</button>
      {selectedFiles.length > 0 && <button className="cancel-btn" onClick={handleCancel}>Cancel</button>}
      </div>
    </div>
  );
}

export default PdfUploader;