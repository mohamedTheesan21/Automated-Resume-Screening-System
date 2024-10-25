import React from 'react';
import { useNavigate } from 'react-router-dom';
import "./Navbar.css"

function Navbar() {
    const navigate = useNavigate();

    const handleClick = () => {
        localStorage.removeItem("token");
        navigate("/login");
    }

    return (
        <div >
            <nav className="navbar navbar-expand-lg nav-bar" style={{height: "10vh"}}>
                <div className="container-fluid">
                    <a className="navbar-brand" href="/home">ARSS</a>
                    <div className="collapse navbar-collapse" id="navbarNav">
                        <ul className="navbar-nav ms-auto">
                            <li className="nav-item">
                                <a className="nav-link" href="/home">Home</a>
                            </li>
                            <li className="nav-item">
                                <a className="nav-link" href="/">About Us</a>
                            </li>
                            <li className="nav-item">
                                <a className="nav-link" href="mailto:info@arss.com">Contact Us</a>
                            </li>
                            <li className="nav-item">
                                <button className="logout-btn" onClick={handleClick}>Log out</button>
                            </li>
                        </ul>
                    </div>
                </div>
            </nav>
        </div>
    )
}

export default Navbar
