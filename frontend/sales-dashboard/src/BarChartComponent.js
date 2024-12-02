import React, { useEffect, useState } from "react";
import { BarChart, Bar, XAxis, YAxis, CartesianGrid, Tooltip, Legend } from "recharts";
import axios from "axios";
import "./BarChartComponent.css"; // Import the CSS file

const BarChartComponent = ({ refreshKey }) => {
  const [data, setData] = useState([]);
  const [loading, setLoading] = useState(true);
  const [error, setError] = useState(null);

  useEffect(() => {
    const fetchData = async () => {
      try {
        setLoading(true); // Show loading spinner while fetching
        const response = await axios.get("http://127.0.0.1:8000/api/bar-chart/");
        setData(response.data);
        setLoading(false);
      } catch (error) {
        setError("Failed to load data.");
        setLoading(false);
      }
    };

    fetchData();
  }, [refreshKey]); // Refresh data when refreshKey changes

  return (
    <div className="bar-chart-container">
      <h2 className="chart-title">Monthly Revenue</h2>

      {loading && <div>Loading...</div>}
      {error && <div>{error}</div>}

      {!loading && !error && (
        <BarChart width={800} height={400} data={data}>
          <CartesianGrid strokeDasharray="3 3" />
          <XAxis dataKey="month" />
          <YAxis />
          <Tooltip />
          <Legend />
          <Bar dataKey="revenue" fill="#82ca9d" />
        </BarChart>
      )}
    </div>
  );
};

export default BarChartComponent;
