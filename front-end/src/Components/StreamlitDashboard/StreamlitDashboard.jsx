import React from "react";

function StreamlitDashboard() {
  return (
    <div className="dashboard" style={{ height: "90vh", width: "100%" }}>
      <iframe
        src="https://automated-resume-screening-system-m0cl.onrender.com"
        width="100%"
        height="100%"
        style={{borderColor: "blue", backgroundColor: "white" }}
        title="Streamlit Dashboard"
      ></iframe>
    </div>
  );
}

export default StreamlitDashboard;
