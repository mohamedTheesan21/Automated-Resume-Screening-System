import React, { useEffect, useState } from "react";
import { useNavigate } from "react-router-dom";
import "./Home.css";
import PdfUploader from "../PdfUploader/PdfUploader";
import Navbar from "../Navbar/Navbar";
import Loading from "../Loading/Loading";
import StreamlitDashboard from "../StreamlitDashboard/StreamlitDashboard";

function Home() {
  // const backendUrl = "https://automated-resume-screening-system-c0w9.onrender.com";
  const backendUrl = "http://127.0.0.1:8000";
  const navigate = useNavigate();
  const [loading, setLoading] = useState(false);
  const [dashboard, setDashboard] = useState(false);

  useEffect(() => {
    const checkAuthentication = async () => {
      const token = localStorage.getItem("token");

      if (!token) {
        console.log("No token found");
        navigate("/");
        return;
      }

      try {
        const response = await fetch(`${backendUrl}/protected`, {
          method: "GET",
          headers: {
            Authorization: `Bearer ${token}`,
          },
        });

        if (response.ok) {
          console.log("User is authenticated");
        } else {
          console.log("User is not authenticated");
          navigate("/");
        }
      } catch (error) {
        console.error("Error fetching user data:", error);
        navigate("/");
      }
    };

    checkAuthentication();
  }, [navigate]);

  return (
    <div>
      <Navbar />
      <div className="home">
        <div className="home-body">
          <div className="home-container">
            <h3>Upload Resumes for Screening</h3>
            <PdfUploader loading={loading} setLoading={setLoading} dashboard={dashboard} setDashboard={setDashboard} />
          </div>
        </div>
        <div className="home-body-right">
          {loading && <Loading />}
          {!loading && (dashboard ? (
            <StreamlitDashboard />
          ) : (
            <div className="about-us-placeholder">
              <div className="about-us-header">
                <h2>Welcome to ARSS</h2>
                <p>Revolutionizing Recruitment with Technology</p>
              </div>
              <div className="about-us-content">
                <h3>How It Works</h3>
                <p>
                  Upload resumes and let our advanced system analyze and rank candidates automatically using AI-powered algorithms.
                </p>
                <div className="icon-list">
                  <div className="icon-item">
                    <span>⚙️</span>
                    <p>Automated resume parsing</p>
                  </div>
                  <div className="icon-item">
                    <span>🔍</span>
                    <p>AI-powered candidate ranking</p>
                  </div>
                  <div className="icon-item">
                    <span>🎯</span>
                    <p>Custom job-specific filters</p>
                  </div>
                  <div className="icon-item">
                    <span>📊</span>
                    <p>Analytics</p>
                  </div>
                </div>
              </div>
              <div className="about-us-footer">
                <p>Start your journey by uploading a resume now to see the magic of automated screening.</p>
              </div>
            </div>
          ))}
        </div>
      </div>
    </div>
  );
}

export default Home;