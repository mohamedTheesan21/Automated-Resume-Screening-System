import React, { useState } from "react";
import "./Signup.css";
// import { useNavigate } from "react-router-dom";

function Signup() {
  //   const navigate = useNavigate();
  const [companyName, setCompanyName] = useState("");
  const [email, setEmail] = useState("");
  const [password, setPassword] = useState("");
  const [confirmPassword, setConfirmPassword] = useState("");

  const handleSubmit = (e) => {};

  return (
    <div className="body">
      <div className="signup-container">
        <div className="header">
          <div className="text">Signup</div>
          <div className="underline"></div>
        </div>
        <form onSubmit={handleSubmit}>
          <div className="input">
            {/* <label>Email</label> */}
            <input
              type="text"
              value={companyName}
              onChange={(e) => setCompanyName(e.target.value)}
              placeholder="Company name"
            />
          </div>
          <div className="input">
            {/* <label>Email</label> */}
            <input
              type="email"
              value={email}
              onChange={(e) => setEmail(e.target.value)}
              placeholder="Email"
            />
          </div>
          <div className="input">
            {/* <label>Email</label> */}
            <input
              type="password"
              value={password}
              onChange={(e) => setPassword(e.target.value)}
              placeholder="Password"
            />
          </div>
          <div className="input">
            {/* <label>Password</label> */}
            <input
              type="password"
              value={confirmPassword}
              onChange={(e) => setConfirmPassword(e.target.value)}
              placeholder="Confirm password"
            />
          </div>

          <div className="signup-submit-container">
            <button type="submit" className="btn">
              Sign Up
            </button>
            <a className="btn" href="/">
              Log In
            </a>
          </div>
        </form>
      </div>
    </div>
  );
}

export default Signup;
