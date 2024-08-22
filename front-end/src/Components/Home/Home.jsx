import React from "react";
import "./Home.css";
import PdfUploader from "../PdfUploader/PdfUploader";

function Home() {
  return (
    <div className="home-body">
      <div className="container" style={{background:"#fff"}}>
        <h1>ARSS</h1>
        <h3>upload Resumes for screening</h3>
        <PdfUploader />
      </div>
    </div>
  );
}

export default Home;
