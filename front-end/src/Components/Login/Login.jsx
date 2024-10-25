import React, { useState } from "react";
import { useNavigate } from "react-router-dom";
import "./Login.css";
import Loading from "../Loading/Loading";

function Login() {
  // const backendUrl = "https://automated-resume-screening-system-c0w9.onrender.com";
  const backendUrl = "http://127.0.0.1:8000";
  const navigate = useNavigate();
  const [showPassword, setShowPassword] = useState(false);
  const [email, setEmail] = useState("");
  const [password, setPassword] = useState("");
  const [error, setError] = useState("");
  const [loading, setLoading] = useState(false)

  const togglePasswordVisibility = () => {
    setShowPassword(!showPassword);
  };

  const hanldeSubmit = async (e) => {
    setLoading(true);
    e.preventDefault();
    const userData = {
      email: email,
      password: password,
    };

    try{
      const response = await fetch(`${backendUrl}/login`, {
        method: "POST",
        headers: {
          "Content-Type": "application/json",
        },
        body: JSON.stringify(userData),
      });
      if (response.ok) {
        const data = await response.json();
        localStorage.setItem("token", data.access_token);
        navigate("/home");
      } else {
        const errorData = await response.json();
        setError(errorData.detail);
        setEmail("");
        setPassword("");
      }
  } catch (error) {
    console.error("Error:", error);
    setError("something went wrong!")
    setEmail("");
    setPassword("");
  }
  setLoading(false);
}

if(loading){
  return <Loading/>
}

  return (
    <div className="body">
      <div className="container">
        <div className="header">
          <div className="text">Login</div>
          <div className="underline"></div>
        </div>
        <form onSubmit={hanldeSubmit}>
          <div className="input">
            <i class="fa-solid fa-envelope fa-xl"></i>
            <input
              type="email"
              value={email}
              onChange={(e) => setEmail(e.target.value)}
              placeholder="Email"
            />
          </div>
          <div className="input" style={{ position: "relative" }}>
            <i class="fa-solid fa-lock fa-xl"></i>
            <input
              type={showPassword ? "text" : "password"}
              value={password}
              onChange={(e) => setPassword(e.target.value)}
              placeholder="Password"
            />
            {showPassword ? (
              <i
                className="far fa-eye eye-icon-signin fa-lg"
                onClick={togglePasswordVisibility}
              ></i>
            ) : (
              <i
                className="fa-regular fa-eye-slash fa-lg eye-icon-signin"
                onClick={togglePasswordVisibility}
              ></i>
            )}
          </div>
          {error && <p className="error">{error}</p>}
          <div className="submit-container">
            <a className="btn change-btn" href="/signup">
              Sign Up
            </a>
            <button type="submit" className="btn submit-btn">
              Log In
            </button>
          </div>
        </form>
      </div>
    </div>
  );
}

export default Login;
