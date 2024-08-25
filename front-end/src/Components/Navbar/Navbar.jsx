import React from 'react';
import "./Navbar.css"

function Navbar() {
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
                                <a className="nav-link" href="/aboutus">About Us</a>
                            </li>
                            <li className="nav-item">
                                <a className="nav-link" href="/contactus">Contact Us</a>
                            </li>
                        </ul>
                    </div>
                </div>
            </nav>
        </div>
    )
}

export default Navbar
