import React from "react";
import Sidebar from "./components/Sidebar";
import "./components/style.css";

function App() {
    const mapURL = "https://nyc-congestion-pricing-backend.onrender.com/static/nyc.html"

    return (
        <div className="dashboard-container">
            <div className="map-container">
                <iframe src={mapURL} width="100%" height="100%" />
            </div>
            <Sidebar />
        </div>
    );
}

export default App;