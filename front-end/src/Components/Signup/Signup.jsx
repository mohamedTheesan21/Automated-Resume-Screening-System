import React, { useState } from "react";
import "./Signup.css";
import { useNavigate } from "react-router-dom";
import Loading from "../Loading/Loading";

function Signup() {
  // const backendUrl = "https://automated-resume-screening-system-c0w9.onrender.com";
  const backendUrl = "http://127.0.0.1:8000";
  const navigate = useNavigate();
  const [companyName, setCompanyName] = useState("");
  const [email, setEmail] = useState("");
  const [password, setPassword] = useState("");
  const [confirmPassword, setConfirmPassword] = useState("");
  const [error, setError] = useState("");
  const [loading, setLoading] = useState(false);

  const setEmpty = () => {
    setPassword("");
    setConfirmPassword("");
  }

  const handleSubmit = async (e) => {
    
    e.preventDefault();
    if (password !== confirmPassword) {
      setError("password and confirm password do not match");
      setEmpty();
      return;
    }

    const userData = {
      name: companyName,
      email: email,
      password: password,
    };
    setLoading(true);
    try {
      const response = await fetch(`${backendUrl}/signup`, {
        method: "POST",
        headers: {
          "Content-Type": "application/json",
        },
        body: JSON.stringify(userData),
      });

      if (response.ok) {
        const data = await response.json();
        console.log(data.msg);
        navigate("/login");
      } else {
        const errorData = await response.json();
        setError(errorData.detail);
        setEmpty();
      }
    } catch (error) {
      console.error("Error:", error);
      setError("something went wrong!");
      setEmpty();
      
    }
    setLoading(false);
  };


  if (loading) {
    return <Loading />;
  }

  return (
    <div className="body">
      <div className="signup-container">
        <div className="header">
          <div className="text">Signup</div>
          <div className="underline"></div>
        </div>
        <form onSubmit={handleSubmit}>
          <div className="input">
            <i class="fa-solid fa-house fa-lg"></i>
            <input
              type="text"
              value={companyName}
              onChange={(e) => setCompanyName(e.target.value)}
              placeholder="Company name"
            />
          </div>
          <div className="input">
            <i class="fa-solid fa-envelope fa-lg"></i>
            <input
              type="email"
              value={email}
              onChange={(e) => setEmail(e.target.value)}
              placeholder="Email"
            />
          </div>
          <div className="input">
            <i class="fa-solid fa-lock fa-lg"></i>
            <input
              type="password"
              value={password}
              onChange={(e) => setPassword(e.target.value)}
              placeholder="Password"
            />
          </div>
          <div className="input">
            <i class="fa-solid fa-lock fa-lg"></i>
            <input
              type="password"
              value={confirmPassword}
              onChange={(e) => setConfirmPassword(e.target.value)}
              placeholder="Confirm password"
            />
          </div>
          {error && <p className="error">{error}</p>}
          <div className="signup-submit-container">
            <button type="submit" className="btn submit-btn">
              Sign Up
            </button>
            <a className="btn change-btn" href="/login">
              Log In
            </a>
          </div>
        </form>
      </div>
    </div>
  );
}

export default Signup;
