import React, { useState, useEffect } from "react";
import DatePicker from "react-datepicker";
import "react-datepicker/dist/react-datepicker.css";
import axios from "axios";
import "./style.css";

function Sidebar() {
    const [preDateRange, setPreDateRange] = useState([new Date(2024, 0, 6), new Date(2024, 0, 6)]);
    const [postDateRange, setPostDateRange] = useState([new Date(2025, 0, 8), new Date(2025, 0, 8)]);
    const [startTime, setStartTime] = useState(6);
    const [endTime, setEndTime] = useState(9);
    const [origin, setOrigin] = useState("bronx");
    const [destination, setDestination] = useState("crz");
    const [plot, setPlot] = useState("destination");
    const [data, setData] = useState("taxi"); 
    const [collapsed, setCollapsed] = useState(false);
    const timeURL = "/time.png"; 
    const scatterURL = "/scatter.png";
    
    const formatDate = (date) => {
        const day = String(date.getDate()).padStart(2, "0");
        const month = String(date.getMonth() + 1).padStart(2, '0');
        const year = date.getFullYear();
        return `${day}-${month}-${year}`;
    };

    const generateData = async () => {
        if (!preDateRange || !postDateRange) {
            alert("Please select a date.");
            return;
        }

        const formattedPreDateRange = `${formatDate(preDateRange[0])},${formatDate(preDateRange[1])}`;
        const formattedPostDateRange = `${formatDate(postDateRange[0])},${formatDate(postDateRange[1])}`;

        try {
            await axios.get("http://127.0.0.1:8000/map", {
                params: {
                    pre: formattedPreDateRange, 
                    post: formattedPostDateRange,
                    start: startTime, 
                    end: endTime, 
                    origin: origin, 
                    destination: destination, 
                    plot: plot, 
                    data: data,
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
            await axios.get("http://127.0.0.1:8000/map", {
                params: {
                    pre: "01-01-2024, 01-01-2024", // Dummy start date
                    post: "01-01-2024, 01-01-2024", // Dummy end date
                    start: "0", // Dummy start time
                    end: "0", // Dummy end time
                    origin: "bronx", // Dummy origin
                    destination: "bronx", // Dummy destination
                    plot: "origin", // Dummy plot
                    data: "taxi", // Dummy data 
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

                        <div className="distribution">
                            <img src={timeURL} alt="Time Distribution" />
                        </div><hr /> 

                        <div className="distribution">
                            <img src={scatterURL} alt="Scatter Plot" />
                        </div><hr /> 

                        <div className="form-container">
                            <div className="column">

                                <label>Pre Congestion Pricing Date: </label><br />
                                <DatePicker
                                    selectsRange
                                    startDate={preDateRange[0]}
                                    endDate={preDateRange[1]}
                                    onChange={(update) => setPreDateRange(update)}
                                    dateFormat="dd/MM/yyyy"
                                    minDate={new Date(2024, 0, 1)}
                                    maxDate={new Date()}
                                    placeholderText="Select date range"
                                /><br />

                                <label>Start Time: </label><br />
                                <input
                                    type="range"
                                    min="0"
                                    max="23"
                                    value={startTime}
                                    onChange={(e) => setStartTime(e.target.value)}
                                />
                                <span>{String(startTime).padStart(2, "0")}:00</span>
                                <br />

                                <label>Origin: </label><br />
                                <input
                                    type="text"
                                    value={origin}
                                    onChange={(e) => setOrigin(e.target.value)}
                                    placeholder="Enter borough or zipcode"
                                /><br />

                            </div>

                            <div className="column">

                                <label>Post Congestion Pricing Date: </label><br />
                                <DatePicker
                                    selectsRange
                                    startDate={postDateRange[0]}
                                    endDate={postDateRange[1]}
                                    onChange={(update) => setPostDateRange(update)}
                                    dateFormat="dd/MM/yyyy"
                                    minDate={new Date(2024, 0, 1)}
                                    maxDate={new Date()}
                                    placeholderText="Select date range"
                                /><br />

                                <label>End Time: </label><br />
                                <input
                                    type="range"
                                    min="0"
                                    max="23"
                                    value={endTime}
                                    onChange={(e) => setEndTime(e.target.value)}
                                />
                                <span>{String(endTime).padStart(2, "0")}:00</span>
                                <br />

                                <label>Destination: </label><br />
                                <input
                                    type="text"
                                    value={destination}
                                    onChange={(e) => setDestination(e.target.value)}
                                    placeholder="Enter borough or zipcode"
                                /><br />

                            </div>
                        </div>

                        <button onClick={() => setPlot(plot === "origin" ? "destination" : "origin")}>
                            {plot}
                        </button><hr />

                        <label>Data: </label><br />
                        <select value={data} onChange={(e) => setData(e.target.value)}>
                            <option value="taxi">Taxi</option>
                            <option value="citibike">Citibike</option>
                        </select><hr />

                        <button onClick={generateData}>Generate</button>

                        <button onClick={clearData}>Clear</button><hr />

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