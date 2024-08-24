import React, { useState } from "react";
import "./Signup.css";
import { useNavigate } from "react-router-dom";

function Signup() {
  const navigate = useNavigate();
  const [companyName, setCompanyName] = useState("");
  const [email, setEmail] = useState("");
  const [password, setPassword] = useState("");
  const [confirmPassword, setConfirmPassword] = useState("");

  const handleSubmit = async (e) => {
    e.preventDefault();
    if (password !== confirmPassword) {
      alert("password are not mathcing");
      return;
    }

    const userData = {
      name: companyName,
      email: email,
      password: password,
    };

    try {
      const response = await fetch("http://127.0.0.1:8000/signup", {
        method: "POST",
        headers: {
          "Content-Type": "application/json",
        },
        body: JSON.stringify(userData),
      });

      if (response.ok) {
        const data = await response.json();
        alert(data.msg);
        navigate("/");
      } else {
        const errorData = await response.json();
        alert(`Error: ${errorData.detail}`);
      }
    } catch (error) {
      console.error("Error:", error);
      alert("Something went wrong!");
    }
  };

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

          <div className="signup-submit-container">
            <button type="submit" className="btn submit-btn">
              Sign Up
            </button>
            <a className="btn change-btn" href="/">
              Log In
            </a>
          </div>
        </form>
      </div>
    </div>
  );
}

export default Signup;
