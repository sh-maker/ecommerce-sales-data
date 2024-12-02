import React, { useState } from "react";
import axios from "axios";
import SummaryMetrics from "./SummaryMetrics";
import LineChartComponents from "./LineChartComponent";
import BarChartComponents from "./BarChartComponent";
import "./ImportCSV.css";

const ImportCSV = () => {
    const [csvFile, setCsvFile] = useState(null);
    const [message, setMessage] = useState(null);
    const [messageType, setMessageType] = useState("");
    const [refreshKey, setRefreshKey] = useState(0); // State to trigger component refresh

    // Handle file change
    const handleFileChange = (e) => {
        const file = e.target.files[0];
        if (file && file.type === "text/csv") {
            setCsvFile(file);
            setMessage(null);
        } else {
            setMessage("Please upload a valid CSV file.");
            setMessageType("error");
        }
    };

    // Handle form submission
    const handleSubmit = async (e) => {
        e.preventDefault();
        if (!csvFile) {
            setMessage("Please upload a CSV file.");
            setMessageType("error");
            return;
        }

        const formData = new FormData();
        formData.append("files", csvFile);

        try {
            const response = await axios.post("http://127.0.0.1:8000/api/import-csv/", formData, {
                headers: { "Content-Type": "multipart/form-data" },
            });

            if (response.data.message === "All CSV files processed successfully") {
                setMessage("CSV files imported successfully!");
                setMessageType("success");

                // Trigger refresh of data after successful upload
                setRefreshKey((prevKey) => prevKey + 1);
            }
        } catch (error) {
            setMessage("Error uploading CSV file.");
            setMessageType("error");
        }
    };

    return (
        <div className="import-csv">
            <h2 className="text-center">Import CSV Data</h2>

            {/* Display success or error message */}
            {message && (
                <div
                    style={{
                        color: messageType === "success" ? "green" : "red",
                        marginBottom: "10px",
                    }}
                >
                    {message}
                </div>
            )}

            {/* CSV Upload Form */}
            {/* <form onSubmit={handleSubmit}>
        <input type="file" accept=".csv" onChange={handleFileChange} />
        <button type="submit">Import Data</button>
      </form> */}
            <form onSubmit={handleSubmit} className="mb-3">
                <div className="row">

                    <div className="col-12 text">
                        
                        <div className="col-10">
                            <input
                                type="file"
                                className="form-control"
                                aria-label="Upload File"
                                aria-describedby="basic-addon1"
                                accept=".csv"
                                onChange={handleFileChange}
                            />
                        </div>
                        <div className="col-2">

                            <button type="submit" className="btn btn-success">
                                Import Data
                            </button>
                        </div>
                    </div>

                </div>

            </form>
            {/* Always Render Metrics and Charts */}
            <SummaryMetrics refreshKey={refreshKey} />
            <LineChartComponents refreshKey={refreshKey} />
            <BarChartComponents refreshKey={refreshKey} />
        </div>
    );
};

export default ImportCSV;
