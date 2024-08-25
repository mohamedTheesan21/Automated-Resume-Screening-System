import React, { useEffect } from "react";
import { useNavigate } from "react-router-dom";
import "./Home.css";
import PdfUploader from "../PdfUploader/PdfUploader";
import Navbar from "../Navbar/Navbar";

function Home() {
  const navigate = useNavigate();

  useEffect(() => {
    const checkAuthentication = async () => {
      const token = localStorage.getItem("token");

      if (!token) {
        // No token, navigate to login
        console.log("No token found");
        navigate("/");
        return;
      }

      try {
        const response = await fetch("http://127.0.0.1:8000/protected", {
          method: "GET",
          headers: {
            "Authorization": `Bearer ${token}`
          }
        });

        if (response.ok) {
          console.log("User is authenticated");
          const user = await response.json();
          console.log(user);
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
