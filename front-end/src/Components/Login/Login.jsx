import React, { useState } from "react";
import { useNavigate } from "react-router-dom";
import "./Login.css";

function Login() {
  const navigate = useNavigate();
  const [showPassword, setShowPassword] = useState(false);
  const [email, setEmail] = useState("");
  const [password, setPassword] = useState("");
  const [error, setError] = useState("");

  const togglePasswordVisibility = () => {
    setShowPassword(!showPassword);
  };

  const hanldeSubmit = async (e) => {
    e.preventDefault();
    const userData = {
      email: email,
      password: password,
    };

    try{
      const response = await fetch("http://127.0.0.1:8000/login", {
        method: "POST",
        headers: {
          "Content-Type": "application/json",
        },
        body: JSON.stringify(userData),
      });
      if (response.ok) {
        const data = await response.json();
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
