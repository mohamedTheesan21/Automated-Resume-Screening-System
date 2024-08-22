import React, { useState } from "react";
import "./Login.css";

function Login() {
  const [showPassword, setShowPassword] = useState(false);
  const [email, setEmail] = useState("");
  const [password, setPassword] = useState("");


  const togglePasswordVisibility = () => {
    setShowPassword(!showPassword);
  };

  const hanldeSubmit = (e) => {
    e.preventDefault();
    console.log(email, password);
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
            {/* <label>Email</label> */}
            <input
              type="email"
              value={email}
              onChange={(e) => setEmail(e.target.value)}
              placeholder="Email"
            />
          </div>
          <div className="input" style={{position: "relative"}}>
            {/* <label>Email</label> */}
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
        

        <div className="submit-container">
          <a className="btn" href="/signup">
            Sign Up
          </a>
          <button type="submit" className="btn">
            Log In
          </button>
        </div>
        </form>
      </div>
    </div>
  );
}

export default Login;
