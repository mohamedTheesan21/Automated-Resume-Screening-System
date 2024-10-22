import React from "react";

function StreamlitDashboard() {
  return (
    <div className="dashboard" style={{ height: "90vh", width: "100%" }}>
      <iframe
        src="http://localhost:8501"
        width="100%"
        height="100%"
        style={{ borderRadius:"30px" , borderColor: "blue", backgroundColor: "white" }}
        title="Streamlit Dashboard"
      ></iframe>
    </div>
  );
}

export default StreamlitDashboard;
