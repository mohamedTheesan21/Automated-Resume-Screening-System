import React from "react";
import "./Home.css";
import PdfUploader from "../PdfUploader/PdfUploader";
import Navbar from "../Navbar/Navbar";

function Home() {
  return (
    <div className="home-body">
      <Navbar />
      <div className="home-container">
        {/* <h1>ARSS</h1> */}
        <h3>upload Resumes for screening</h3>
        <PdfUploader />
      </div>
    </div>
  );
}

export default Home;
