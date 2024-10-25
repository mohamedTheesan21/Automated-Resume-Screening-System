import React from "react";
import { Link } from "react-router-dom";
import "./Aboutus.css";

const AboutUs = () => {
  return (
    <div className="about-us-container">
      {/* Navigation Bar */}
      <nav className="aboutus-navbar">
        <div className="aboutus-navbar-logo">
          <Link to="/">ARSS</Link>
        </div>
        <div className="aboutus-navbar-links">
          <Link to="/login" className="login-button">Login</Link>
        </div>
      </nav>

      <section className="hero-section">
        <div className="overlay">
          <h1>ARSS</h1>
          <p>Revolutionizing Recruitment with Technology</p>
        </div>
      </section>

      <section className="about-us-details">
        <div className="about-us-content">
          <h2>What is ARSS?</h2>
          <p>
            The Automated Resume Screening System (ARSS) is an innovative platform that transforms the way resumes are screened. Using state-of-the-art Natural Language Processing (NLP) and machine learning algorithms, ARSS automates the resume review process, helping recruiters find top candidates quickly and efficiently.
          </p>
        </div>
        
        <div className="features">
          <h2>Key Features</h2>
          <ul className="features-list">
            <li>⚙️ Automated resume parsing and keyword extraction</li>
            <li>🔍 AI-powered candidate ranking and recommendations</li>
            <li>🎯 Customizable filters for job-specific screening</li>
            <li>📊 Real-time analytics and candidate insights dashboard</li>
          </ul>
        </div>

        <div className="mission">
          <h2>Our Mission</h2>
          <p>
            At ARSS, we aim to revolutionize recruitment by offering a seamless, data-driven solution for companies to find the right talent. Our goal is to simplify hiring, empowering businesses to focus on what matters – connecting with the right candidates.
          </p>
        </div>

        <div className="contact-info">
          <h2>Contact Us</h2>
          <p>If you'd like to know more or have any questions, feel free to reach out:</p>
          <a className="email-link" href="mailto:info@arss.com">info@arss.com</a>
        </div>
      </section>
    </div>
  );
};

export default AboutUs;
