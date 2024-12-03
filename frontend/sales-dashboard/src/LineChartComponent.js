import React, { useState, useEffect } from "react";
import { LineChart, Line, XAxis, YAxis, CartesianGrid, Tooltip, Legend } from "recharts";
import axios from "axios";
import "./LineChartComponent.css"; // Import the CSS file

const LineChartComponent = ({ refreshKey }) => {
  const [data, setData] = useState([]);
  const [loading, setLoading] = useState(true);
  const [error, setError] = useState(null);

  // Fetch data from the API
  useEffect(() => {
    const fetchData = async () => {
      try {
        setLoading(true); // Set loading to true before fetching data
        const response = await axios.get("http://127.0.0.1:8000/api/line-chart/");
        setData(response.data);
        setLoading(false);
      } catch (error) {
        setError("Failed to load data.");
        setLoading(false);
      }
    };

    fetchData();
  }, [refreshKey]); // Add refreshKey to the dependency array

  // Render the chart or loading/error message
  return (
    <div className="chart-container">
      <h2>Monthly Sales Volume</h2>

      {loading && <div>Loading...</div>}
      {error && <div>{error}</div>}

      {!loading && !error && (
        <LineChart width={800} height={400} data={data}>
          <CartesianGrid strokeDasharray="3 3" />
          <XAxis dataKey="month" />
          <YAxis />
          <Tooltip />
          <Legend />
          <Line
            type="monotone"
            dataKey="quantity_sold"
            stroke="#8884d8"
            activeDot={{ r: 8 }}
          />
        </LineChart>
      )}
    </div>
  );
};

export default LineChartComponent;
