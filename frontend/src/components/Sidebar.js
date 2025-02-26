import React, { useState } from "react";
import DatePicker from "react-datepicker";
import "react-datepicker/dist/react-datepicker.css";
import axios from "axios";
import "./style.css";

const API_URL = process.env.REACT_APP_API_URL || "http://127.0.0.1:8000";

function Sidebar() {
    const [postDate, setPostDate] = useState(new Date(2024, 0));
    const [PUBorough, setPUBorough] = useState("Bronx");
    const [DOBorough, setDOBorough] = useState("Bronx"); 
    const [plot, setPlot] = useState("Pickup");
    const [toggle, setToggle] = useState("Peak");
    const [collapsed, setCollapsed] = useState(false);
    const timeURL = "https://nyc-congestion-pricing-backend.onrender.com/time.png";
    
    const formatDate = (date) => {
        const month = String(date.getMonth() + 1).padStart(2, '0');
        const year = date.getFullYear();
        return `${month}-${year}`;
    };

    const generateData = async () => {
        if (!postDate) {
            alert("Please select a date.");
            return;
        }

        const formattedDate = formatDate(postDate);

        try {
            await axios.get(`${API_URL}/taxi`, {
                params: {
                    date: formattedDate,
                    pu_borough: PUBorough,
                    do_borough: DOBorough,
                    plot: plot,
                    hours: toggle,
                    clear: 0
                }
            });
            window.location.reload();

        } catch (error) {
            console.error("Error fetching data:", error);
            alert("Failed to generate data.");
        }
    };

    const clearData = async () => {
        try {
            await axios.get(`${API_URL}/taxi`, {
                params: {
                    date: "01-2024", // Dummy date
                    pu_borough: "bronx", // Dummy borough
                    do_borough: "bronx", // Dummy borough
                    plot: "Pickup", // Dummy plot
                    hours: "Peak", // Dummy hours
                    clear: 1
                }
            });
            window.location.reload();

        } catch (error) {
            console.error("Error fetching data:", error);
            alert("Failed to clear data.");
        }
    };

    return (
        <>
            <div className={`sidebar ${collapsed ? "collapsed" : ""}`}>
                {!collapsed && (
                    <>
                        <h1>NYC Congestion Pricing Dashboard</h1>

                        <label>Month:</label><br />
                        <DatePicker
                            selected={postDate}
                            onChange={(date) => setPostDate(date)}
                            dateFormat="MM/yyyy"
                            showMonthYearPicker
                            showFullMonthYearPicker
                            dropdownMode="select"
                            minDate={new Date(2024, 0)}
                            maxDate={new Date()}
                        /><hr />

                        <h2>Taxi</h2>
                        <label>Pick Up Borough:</label><br />
                        <select value={PUBorough} onChange={(e) => setPUBorough(e.target.value)}>
                            <option value="bronx">Bronx</option>
                            <option value="brooklyn">Brooklyn</option>
                            <option value="crz">Congestion Relief Zone</option>
                            <option value="manhattan">Manhattan</option>
                            <option value="queens">Queens</option>
                            <option value="staten_island">Staten Island</option>
                        </select><br />

                        <label>Drop Off Borough:</label><br />
                        <select value={DOBorough} onChange={(e) => setDOBorough(e.target.value)}>
                            <option value="bronx">Bronx</option>
                            <option value="brooklyn">Brooklyn</option>
                            <option value="crz">Congestion Relief Zone</option>
                            <option value="manhattan">Manhattan</option>
                            <option value="queens">Queens</option>
                            <option value="staten_island">Staten Island</option>
                        </select><br />

                        <button onClick={() => setPlot(plot === "Pickup" ? "Dropoff" : "Pickup")}>
                            {plot}
                        </button><hr />

                        <button onClick={() => setToggle(toggle === "Peak" ? "Overnight" : "Peak")}>
                            {toggle}
                        </button><hr />

                        <button onClick={generateData}>Generate</button>

                        <button onClick={clearData}>Clear</button><hr />

                        <div className="time-distribution">
                            <img src={timeURL} alt="Time Distribution" />
                        </div>
                    </>
                )}
            </div>

            <button className={`collapse-button ${collapsed ? "collapsed-btn" : ""}`} onClick={() => setCollapsed(!collapsed)}>
                {collapsed ? "→" : "←"}
            </button>
        </>
    );
}

export default Sidebar;