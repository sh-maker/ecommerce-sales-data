import React, { useEffect, useState } from "react";
import axios from "axios";
import "./SummaryMetrics.css";

const SummaryMetrics = ({ refreshKey }) => {
  const [metrics, setMetrics] = useState({});

  useEffect(() => {
    // Fetch summary metrics whenever refreshKey changes
    axios
      .get("http://127.0.0.1:8000/api/summary-metrics/")
      .then((response) => setMetrics(response.data))
      .catch((error) => console.error(error));
  }, [refreshKey]); // Dependency array includes refreshKey

  return (
    <div className="metrics-container">
      <h2>Summary Metrics</h2>
      <div className="cards">
        <div className="card">
          <h3>Total Revenue</h3>
          <p>{metrics.total_revenue}</p>
        </div>
        <div className="card">
          <h3>Total Orders</h3>
          <p>{metrics.total_orders}</p>
        </div>
        <div className="card">
          <h3>Total Products Sold</h3>
          <p>{metrics.total_products_sold}</p>
        </div>
        <div className="card">
          <h3>Canceled Order Percentage</h3>
          <p>{metrics.canceled_order_percentage}%</p>
        </div>
      </div>
    </div>
  );
};

export default SummaryMetrics;
