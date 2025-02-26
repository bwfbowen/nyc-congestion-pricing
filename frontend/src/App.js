import React from "react";
import Sidebar from "./components/Sidebar";
import "./components/style.css";

function App() {
    const mapURL = "https://nyc-congestion-pricing-backend.onrender.com/nyc.html"

    return (
        <div className="dashboard-container">
            <div className="map-container">
                <iframe src={mapURL} width="100%" height="100%" title="NYC"/>
            </div>
            <Sidebar />
        </div>
    );
}

export default App;