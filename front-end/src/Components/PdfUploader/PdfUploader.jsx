import React, { useState } from "react";
import "./PdfUploader.css";

function PdfUploader({setLoading, setDashboard}) {
  const backendUrl = "https://automated-resume-screening-system-c0w9.onrender.com"
  const [selectedFiles, setSelectedFiles] = useState([]);
  const [skills, setSkills] = useState("");
  const [education, setEducation] = useState("");
  const [experience, setExperience] = useState("");
  

  const handleFileChange = (event) => {
    setSelectedFiles(Array.from(event.target.files));
  };

  const handleFileUpload = async() => {
    setLoading(true);
    if (selectedFiles.length > 0) {
      const formData = new FormData();
      selectedFiles.forEach((file) => {
        formData.append("files", file);
      });

      try {
        const response = await fetch(`${backendUrl}/upload`, {
          method: "POST",
          body: formData,
        });
        if (response.ok) {
          const data = await response.json();
          console.log(data.msg);
          console.log(data.file_ids);
        } else {
          const data = await response.json();
          console.log(data.details);
        }
      } catch (error) {
        console.log(error);
      }
    }
    setLoading(false);
    setDashboard(true);
  };

  const handleDrop = (event) => {
    event.preventDefault();
    const files = Array.from(event.dataTransfer.files).filter(
      (file) => file.type === "application/pdf"
    );
    setSelectedFiles((prevFiles) => [...prevFiles, ...files]);
  };

  const handleDragOver = (event) => {
    event.preventDefault();
  };

  const handleCancel = () => {
    setSelectedFiles([]);
  };

  // if (loading) {
  //   return <Loading />;
  // }

  return (
    <div className="pdf-uploader-container">
      {!selectedFiles.length > 0 && (
        <div>
          <input
            type="file"
            accept=".pdf"
            multiple
            onChange={handleFileChange}
            style={{ display: "none" }}
            id="file-input"
            required
          />
          <label
            className="file-input-label"
            htmlFor="file-input"
            onDrop={handleDrop}
            onDragOver={handleDragOver}
          >
            Drag and drop your PDFs here or click to select files <br />
            <br /> <i class="fa-solid fa-upload bounce fa-xl"></i>
          </label>{" "}
        </div>
      )}
      {selectedFiles.length > 0 && (
        <ul className="pdfs">
          {selectedFiles.map((file, index) => (
            <li key={index}>
              <i class="fa-solid fa-file-pdf" style={{ color: "#da1010" }}></i>{" "}
              {file.name}
            </li>
          ))}
        </ul>
      )}
      {selectedFiles.length > 0 && (
        <button className="cancel-btn" onClick={handleCancel}>
          Cancel
        </button>
      )}
      <input
        className="job-description"
        type="text"
        value={skills}
        onChange={(e) => setSkills(e.target.value)}
        placeholder="Skills"
        required
      />
      <input
        className="job-description"
        type="text"
        value={education}
        onChange={(e) => setEducation(e.target.value)}
        placeholder="Education"
        required
      />
      <input
        className="job-description"
        type="text"
        value={experience}
        onChange={(e) => setExperience(e.target.value)}
        placeholder="Experience"
        required
      />
      <div className="buttons">
        <button
          className="upload-btn"
          onClick={handleFileUpload}
          style={{ marginBottom: "10px" }}
        >
          Upload CVs
        </button>
      </div>
    </div>
  );
}

export default PdfUploader;
